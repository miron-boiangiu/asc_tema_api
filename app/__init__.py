import os
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.query_handler import QueryHandler
from app.routes import queries_blueprint

OUTPUT_FOLDER = "./results"

def create_app(test_config=None):
    
    webserver = Flask(__name__)

    tasks_runner = ThreadPool()
    data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

    try:
        os.makedirs(OUTPUT_FOLDER)
    except FileExistsError:
        pass

    webserver.query_handler = QueryHandler(tasks_runner, data_ingestor, OUTPUT_FOLDER)
    webserver.register_blueprint(queries_blueprint, url_prefix='/')

    return webserver
