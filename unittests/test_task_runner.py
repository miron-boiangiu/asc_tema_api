import unittest
import time
from threading import Event
from app.task_runner import Task, ThreadPool

class ThreadPoolTest(unittest.TestCase):

    class ExampleTask(Task):
        def __init__(self) -> None:
            self.event = Event()
        
        def run(self):
            self.event.set()

    def setUp(self) -> None:
        self.thread_pool = ThreadPool()

    def test_run_example_task(self) -> None:
        example_task = ThreadPoolTest.ExampleTask()

        self.thread_pool.push_task(example_task)
        
        timeout_time = 5
        interval_time = 0.05
        for i in range(0, int(timeout_time//interval_time)):
            time.sleep(interval_time)
            print(i)
            if example_task.event.is_set():
                break

        self.assertTrue(example_task.event.is_set())

        self.thread_pool.terminate()
