"""
Contains the query handler and his friends.
"""


import os
from threading import Lock, Event
from app import ThreadPool
from app import DataIngestor
from app.tasks import Best5Task, Worst5Task, StatesMeanTask, StateMeanTask,\
    GlobalMeanTask, DiffFromMeanTask, StateDiffFromMeanTask, StateMeanByCategory,\
    MeanByCategory


class NonexistentQueryException(Exception):
    """
    Exception for when a query does not exist.
    """


class HandlerTerminatedException(Exception):
    """
    Exception for when illegal actions are taken on
    the handler after its termination.
    """

class QueryHandler:
    """
    The backbone of the API, creates and manages tasks in order to
    respond to queries.
    """

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

    def __init__(self, threadpool: ThreadPool, data_ingestor: DataIngestor, output_folder = None):
        self._threadpool = threadpool
        self._data_ingestor = data_ingestor
        self._tasks = {}
        self._next_assignable_task_no = 1
        self._mutex = Lock()
        self._terminated = Event()
        self._output_folder = output_folder

    def handle_query(self, query, request_json):
        """
        Receives a query type and its data and returns an id for fetching the results later.
        """

        if self._terminated.is_set():
            raise HandlerTerminatedException()

        with self._mutex:

            file_name = f"job_id_{self._next_assignable_task_no}"

            if self._output_folder:
                output_path = os.path.join(self._output_folder, file_name)
            else:
                output_path = None

            new_task = QueryHandler.query_to_task_translator[query](self._data_ingestor,
                                                                    output_path=output_path,
                                                                    **request_json)
            self._threadpool.push_task(new_task)
            self._tasks[self._next_assignable_task_no] = new_task

            new_id = self._next_assignable_task_no
            self._next_assignable_task_no += 1

        return new_id

    def query_exists(self, query_id):
        """
        Check if a query with a specific id exists.
        """

        query_id = int(query_id)
        return query_id in self._tasks

    def is_query_finished(self, query_id):
        """
        Checks if a specific query is done.
        """

        query_id = int(query_id)
        if not self.query_exists(query_id):
            raise NonexistentQueryException()

        return self._tasks[query_id].is_done()

    def get_query_result(self, query_id):
        """
        Returns the results of the query with the specified id.
        """

        query_id = int(query_id)
        if not self.query_exists(query_id):
            raise NonexistentQueryException()

        return self._tasks[query_id].get_result()

    def all_queries_status(self):
        """
        Returns data on the status of all existing queries.
        """

        result = []

        for task_no, task in self._tasks.items():
            status = "done" if task.is_done else "running"
            key = f"job_id_{task_no}"
            result.append({key: status})

        return result

    def unfinished_query_count(self):
        """
        Returns the number of queries that have not yet been done.
        """

        unfinished_tasks_no = 0

        for task_no, task in self._tasks.items():
            if not task.is_done():
                unfinished_tasks_no += 1

        return unfinished_tasks_no

    def terminate(self):
        """
        Stop accepting new queries.
        """

        #  We stop accepting new requests
        self._terminated.set()

        # We tell the threadpool to finish work and terminate.
        self._threadpool.terminate()
