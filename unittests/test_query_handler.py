import unittest
import time
from app.query_handler import QueryHandler, ThreadPool, DataIngestor, NonexistentQueryException


class QueryHandlerTest(unittest.TestCase):

    def setUp(self) -> None:
        threadpool = ThreadPool()
        data_ingestor = DataIngestor('./unittests/test_data.csv')
        self._query_handler = QueryHandler(threadpool, data_ingestor)

    def tearDown(self) -> None:
        self._query_handler.terminate()

    def test_query_is_run(self) -> None:
        question = "Percent of adults who engage in no leisure-time physical activity"
        query_id = self._query_handler.handle_query("best5", {"question": question})

        self.assertTrue(self._query_handler.query_exists(query_id))

        timeout_time = 5
        interval_time = 0.05
        for i in range(0, int(timeout_time//interval_time)):
            time.sleep(interval_time)
            if self._query_handler.is_query_finished(query_id):
                break

        self.assertTrue(self._query_handler.is_query_finished(query_id))
        self.assertNotEqual(len(self._query_handler.get_query_result(query_id)), 0)

    def test_when_query_exists_on_nonexistent_query_then_return_false(self) -> None:
        self.assertFalse(self._query_handler.query_exists(1))

    def test_when_is_query_finished_on_nonexistent_query_then_raise_exception(self) -> None:
        with self.assertRaises(NonexistentQueryException):
            self._query_handler.is_query_finished(1)

    def test_when_get_query_result_on_nonexistent_query_then_raise_exception(self) -> None:
        with self.assertRaises(NonexistentQueryException):
            self._query_handler.get_query_result(1)
