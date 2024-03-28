import os
from queue import Queue, Empty
from threading import Thread, Event


class Task():
    def run(self):
        pass


class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        self._tasks_queue: Queue = Queue()
        self._terminate_event = Event()
        self._workers: list[TaskRunner] = []

        self._start_workers()

    def _start_workers(self):
        number_of_threads = 0

        if "TP_NUM_OF_THREADS" in os.environ:
            number_of_threads = os.getenv("TP_NUM_OF_THREADS")
        else:
            number_of_threads = os.cpu_count()

        for worker_no in range(0, number_of_threads):
            new_worker = TaskRunner(self)
            self._workers.append(new_worker)
            new_worker.start()

    def push_task(self, task: Task) -> None:
        self._tasks_queue.put(task)

    def _pop_task(self) -> Task:
        return self._tasks_queue.get(block=False)
    
    def _is_terminated(self) -> bool:
        return self._terminate_event.is_set()

    def terminate(self) -> None:
        self._terminate_event.set()
        for worker in self._workers:
            worker.join()


class TaskRunner(Thread):

    def __init__(self, threadpool: ThreadPool):
        Thread.__init__(self)
        self._threadpool: ThreadPool = threadpool

    def run(self):
        while True:
            try:
                task_to_run = self._threadpool._pop_task()
                task_to_run.run()
            except Empty:
                pass

            if self._threadpool._is_terminated():
                break
