import os
from threading import Lock, Event
from app import ThreadPool
from app import DataIngestor
from app.task_runner import Task
from app.tasks import Best5Task, Worst5Task, StatesMeanTask, StateMeanTask,\
    GlobalMeanTask, DiffFromMeanTask, StateDiffFromMeanTask, StateMeanByCategory, \
    MeanByCategory


class NonexistentQueryException(Exception):
    def __init__(self):            
        super().__init__()

class HandlerTerminatedException(Exception):
    def __init__(self):            
        super().__init__()

class QueryHandler:

    query_to_task_translator = {
        "best5": Best5Task,
        "worst5": Worst5Task,
        "states_mean": StatesMeanTask,
        "state_mean": StateMeanTask,
        "global_mean": GlobalMeanTask,
        "diff_from_mean": DiffFromMeanTask,
        "state_diff_from_mean": StateDiffFromMeanTask,
        "state_mean_by_category" : StateMeanByCategory,
        "mean_by_category": MeanByCategory,
    }

    def __init__(self, threadpool: ThreadPool, data_ingestor: DataIngestor, output_folder = None) -> None:
        self._threadpool = threadpool
        self._data_ingestor = data_ingestor
        self._tasks: dict[int, Task] = {}
        self._next_assignable_task_no = 1
        self._mutex = Lock()
        self._terminated = Event()
        self._output_folder = output_folder

    def handle_query(self, query: str, request_json: dict):
        
        if self._terminated.is_set():
            raise HandlerTerminatedException()

        with self._mutex:
            
            file_name = f"job_id_{self._next_assignable_task_no}"
            output_path = os.path.join(self._output_folder, file_name)

            new_task = QueryHandler.query_to_task_translator[query](self._data_ingestor, output_path=output_path, **request_json)
            self._threadpool.push_task(new_task)
            self._tasks[self._next_assignable_task_no] = new_task

            id = self._next_assignable_task_no
            self._next_assignable_task_no += 1

        return id
    
    def query_exists(self, query_id) -> bool:
        query_id = int(query_id)
        return query_id in self._tasks

    def is_query_finished(self, query_id) -> bool:
        query_id = int(query_id)
        if not self.query_exists(query_id):
            raise NonexistentQueryException()

        return self._tasks[query_id].is_done()

    def get_query_result(self, query_id):
        query_id = int(query_id)
        if not self.query_exists(query_id):
            raise NonexistentQueryException()

        return self._tasks[query_id].get_result()
    
    def all_queries_status(self) -> list[dict[str: str]]:
        result = []

        for task_no, task in self._tasks.items():
            status = "done" if task.is_done else "running"
            key = f"job_id_{task_no}"
            result.append({key: status})

        return result

    def unfinished_query_count(self) -> int:
        unfinished_tasks_no = 0

        for task_no, task in self._tasks.items():
            if not task.is_done():
                unfinished_tasks_no += 1
    
        return unfinished_tasks_no

    def terminate(self):
        #  We stop accepting new requests
        self._terminated.set()

        # We tell the threadpool to finish work and terminate.
        self._threadpool.terminate()
