import os
import time
import logging
import logging.handlers
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.query_handler import QueryHandler
from app.routes import queries_blueprint


DATASET_PATH = "./nutrition_activity_obesity_usa_subset.csv"

LOGGING_OUTPUT_FOLDER = "./results"
LOGGING_OUTPUT_FORMAT = '%(levelname)s:%(asctime)s:%(message)s'
LOGGING_FILESIZE = 204800  # 200 kB
LOGGING_BACKUP_COUNT = 5
LOGGING_FILENAME = 'webserver.log'

def create_app(test_config=None, debug=False):

    webserver = Flask(__name__)

    persistent_logger = logging.getLogger(__name__)

    formatter = logging.Formatter(LOGGING_OUTPUT_FORMAT)
    formatter.converter = time.gmtime

    file_handler = logging.handlers.RotatingFileHandler(LOGGING_FILENAME, "a", LOGGING_FILESIZE, LOGGING_BACKUP_COUNT, "utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    persistent_logger.addHandler(file_handler)
    persistent_logger.setLevel(logging.INFO)

    tasks_runner = ThreadPool()
    data_ingestor = DataIngestor(DATASET_PATH)

    try:
        os.makedirs(LOGGING_OUTPUT_FOLDER)
    except FileExistsError:
        pass

    webserver.query_handler = QueryHandler(tasks_runner, data_ingestor, LOGGING_OUTPUT_FOLDER)
    webserver.persistent_logger = persistent_logger
    webserver.register_blueprint(queries_blueprint, url_prefix='/')

    return webserver
