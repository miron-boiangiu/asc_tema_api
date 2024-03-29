from threading import Lock
from app import ThreadPool
from app import DataIngestor
from app.task_runner import Task
from app.tasks import Best5Task


class NonexistentQueryException(Exception):
    def __init__(self):            
        super().__init__()


class QueryHandler:

    query_to_task_translator = {
        "best5": Best5Task,
    }

    def __init__(self, threadpool: ThreadPool, data_ingestor: DataIngestor) -> None:
        self._threadpool = threadpool
        self._data_ingestor = data_ingestor
        self._tasks: dict[int, Task] = {}
        self._next_assignable_task_no = 1
        self._mutex = Lock()

    def handle_query(self, query: str, request_json: dict):
        
        new_task = QueryHandler.query_to_task_translator[query](self._data_ingestor, **request_json)
        self._threadpool.push_task(new_task)
        self._tasks[self._next_assignable_task_no] = new_task

        with self._mutex:
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
    
    def terminate(self):
        self._threadpool.terminate()
