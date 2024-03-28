from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

if __name__ == "__main__":
    
    webserver = Flask(__name__)

    webserver.tasks_runner = ThreadPool()

    webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

    webserver.job_counter = 1

    from app import routes
