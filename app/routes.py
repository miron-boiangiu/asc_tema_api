"""
All routes for the data processing API.
"""


from flask import request, Blueprint, current_app
from app.query_handler import NonexistentQueryException, HandlerTerminatedException
from app.response_formats import error_response, data_response, running_response, job_id_response,\
    INVALID_JOB_ID_REASON, NO_QUESTION_REASON, NO_STATE_REASON, HANDLER_TERMINATED_EXCEPTION
from app.logger_strings import LOGGER_SHUTTING_DOWN, LOGGER_NONEXISTENT_QUERY_ERROR,\
    LOGGER_REQUEST_MISSING_FIELD, LOGGER_HANDLER_TERMINATED_ERROR, LOGGER_CALL_STARTED,\
    LOGGER_CALL_ENDED


queries_blueprint = Blueprint('queries', __name__)

@queries_blueprint.route('/api/graceful_shutdown', methods=['GET'])
def shutdown_request():

    current_app.persistent_logger.warning(LOGGER_SHUTTING_DOWN)
    current_app.query_handler.terminate()
    return data_response("terminated")

@queries_blueprint.route('/api/jobs', methods=['GET'])
def jobs_request():

    return data_response(current_app.query_handler.all_queries_status())

@queries_blueprint.route('/api/num_jobs', methods=['GET'])
def num_jobs_request():

    return data_response(current_app.query_handler.unfinished_query_count())

@queries_blueprint.route('/api/get_results/job_id_<job_id>', methods=['GET'])
def get_results_request(job_id):

    try:
        if current_app.query_handler.is_query_finished(job_id):
            return data_response(current_app.query_handler.get_query_result(job_id))

        return running_response()

    except NonexistentQueryException:
        current_app.persistent_logger.error(LOGGER_NONEXISTENT_QUERY_ERROR)
        return error_response(INVALID_JOB_ID_REASON), 404

# If you change a route, also change it in query_handler.py's query_to_task_translator!
@queries_blueprint.route('/api/best5', methods=['POST'])
@queries_blueprint.route('/api/states_mean', methods=['POST'])
@queries_blueprint.route('/api/worst5', methods=['POST'])
@queries_blueprint.route('/api/global_mean', methods=['POST'])
@queries_blueprint.route('/api/diff_from_mean', methods=['POST'])
@queries_blueprint.route('/api/mean_by_category', methods=['POST'])
def general_question_request():

    if "question" not in request.json:
        current_app.persistent_logger.error(LOGGER_REQUEST_MISSING_FIELD, "question")
        return error_response(NO_QUESTION_REASON), 400

    type_of_request = request.path.split("/")[-1]

    try:
        job_id = current_app.query_handler.handle_query(type_of_request, request.json)
    except HandlerTerminatedException:
        current_app.persistent_logger.error(LOGGER_HANDLER_TERMINATED_ERROR)
        return error_response(HANDLER_TERMINATED_EXCEPTION), 409

    return job_id_response(job_id)

# If you change a route, also change it in query_handler.py's query_to_task_translator!
@queries_blueprint.route('/api/state_mean', methods=['POST'])
@queries_blueprint.route('/api/state_diff_from_mean', methods=['POST'])
@queries_blueprint.route('/api/state_mean_by_category', methods=['POST'])
def particular_state_question_request():

    if "question" not in request.json:
        current_app.persistent_logger.error(LOGGER_REQUEST_MISSING_FIELD, "question")
        return error_response(NO_QUESTION_REASON), 400

    if "state" not in request.json:
        current_app.persistent_logger.error(LOGGER_REQUEST_MISSING_FIELD, "state")
        return error_response(NO_STATE_REASON), 400

    type_of_request = request.path.split("/")[-1]

    try:
        job_id = current_app.query_handler.handle_query(type_of_request, request.json)
    except HandlerTerminatedException:
        current_app.persistent_logger.error(LOGGER_HANDLER_TERMINATED_ERROR)
        return error_response(HANDLER_TERMINATED_EXCEPTION), 409

    return job_id_response(job_id)

@queries_blueprint.before_request
def before_query():
    current_app.persistent_logger.info(LOGGER_CALL_STARTED, request.path)

@queries_blueprint.after_request
def after_query(response):
    current_app.persistent_logger.info(LOGGER_CALL_ENDED)
    return response
