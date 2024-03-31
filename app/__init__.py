import os
import time
import logging
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.query_handler import QueryHandler
from app.routes import queries_blueprint

OUTPUT_FOLDER = "./results"
OUTPUT_FORMAT = '%(levelname)s:%(asctime)s:%(message)s'

def create_app(test_config=None, debug=False):
    
    webserver = Flask(__name__)

    persistent_logger = logging.getLogger(__name__)
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(filename='webserver.log', format=OUTPUT_FORMAT, encoding='utf-8', level=logging.INFO)

    tasks_runner = ThreadPool()
    data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

    try:
        os.makedirs(OUTPUT_FOLDER)
    except FileExistsError:
        pass

    webserver.query_handler = QueryHandler(tasks_runner, data_ingestor, OUTPUT_FOLDER)
    webserver.persistent_logger = persistent_logger
    webserver.register_blueprint(queries_blueprint, url_prefix='/')

    return webserver
