"""
Generic ThreadPool for solving tasks.
"""


import os
from queue import Queue, Empty
from threading import Thread, Event, Lock


class Task:
    """
    Generic task to be solved by a TaskRunner.
    """

    def __init__(self) -> None:
        self._is_done_event = Event()
        self._result = None

    def is_done(self) -> bool:
        return self._is_done_event.is_set()

    def get_result(self):
        return self._result

    def _done(self):
        self._is_done_event.set()

    def run(self):
        pass

    def after_running(self):
        pass

    def start(self):
        self._result = self.run()
        self.after_running()
        self._done()


class ThreadPool:
    """
    TaskRunner spawner and Tasks container.
    """

    def __init__(self):
        self._tasks_queue: Queue = Queue()
        self._terminate_event = Event()
        self._workers = []
        self._wakeup_workers = Event()
        self._safety_mutex = Lock()  # Necessary because we do multiple things in push() and pop()
        self._start_workers()

    def _start_workers(self):
        number_of_threads = 0

        if "TP_NUM_OF_THREADS" in os.environ:
            number_of_threads = int(os.getenv("TP_NUM_OF_THREADS"))
        else:
            number_of_threads = os.cpu_count()

        for worker_no in range(0, number_of_threads):
            new_worker = TaskRunner(self, self._wakeup_workers)
            self._workers.append(new_worker)
            new_worker.start()

    def push_task(self, task: Task) -> None:
        with self._safety_mutex:
            self._tasks_queue.put(task)
            self._wakeup_workers.set()

    def _pop_task(self) -> Task:
        with self._safety_mutex:
            task = self._tasks_queue.get(block=False)
            if self._tasks_queue.qsize() == 0 and not self._terminate_event.is_set():
                self._wakeup_workers.clear()
            return task

    def tasks_left(self) -> int:
        return self._tasks_queue.qsize()

    def _is_terminated(self) -> bool:
        return self._terminate_event.is_set()

    def terminate(self) -> None:
        """
        Finishes given tasks and terminates.
        """
        with self._safety_mutex:
            self._terminate_event.set()
            self._wakeup_workers.set()

        # Should we really join them here? They terminate once no more
        # tasks are left anyway, which can be queried by users.
        for worker in self._workers:
            worker.join()


class TaskRunner(Thread):
    """
    Worker that continuously solves tasks from its parent ThreadPool.
    """

    def __init__(self, threadpool: ThreadPool, wakeup_event: Event):
        Thread.__init__(self)
        self._threadpool: ThreadPool = threadpool
        self._wakeup_event = wakeup_event

    def run(self):
        while True:

            self._wakeup_event.wait()
            try:
                task_to_run = self._threadpool._pop_task()
                task_to_run.start()
            except Empty:
                pass

            if self._threadpool._is_terminated() and self._threadpool.tasks_left() == 0:
                break
