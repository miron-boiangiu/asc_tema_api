import os
import json

from flask import request, jsonify, Blueprint, current_app
from app.query_handler import NonexistentQueryException, HandlerTerminatedException
from app.response_formats import error_response, data_response, running_response, job_id_response,\
    INVALID_JOB_ID_REASON, NO_QUESTION_REASON, NO_STATE_REASON, HANDLER_TERMINATED_EXCEPTION


queries_blueprint = Blueprint('queries', __name__)

@queries_blueprint.route('/api/graceful_shutdown', methods=['GET'])
def shutdown_request():

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
        else:
            return running_response()

    except NonexistentQueryException:
        return error_response(INVALID_JOB_ID_REASON)

@queries_blueprint.route('/api/best5', methods=['POST'])
def best5_request():

    if "question" not in request.json:
        return error_response(NO_QUESTION_REASON)

    try:
        id = current_app.query_handler.handle_query("best5", request.json)
    except HandlerTerminatedException:
        return error_response(HANDLER_TERMINATED_EXCEPTION)

    return job_id_response(id)

@queries_blueprint.route('/api/states_mean', methods=['POST'])
def states_mean_request():

    if "question" not in request.json:
        return error_response(NO_QUESTION_REASON)

    try:
        id = current_app.query_handler.handle_query("states_mean", request.json)
    except HandlerTerminatedException:
        return error_response(HANDLER_TERMINATED_EXCEPTION)

    return job_id_response(id)

@queries_blueprint.route('/api/state_mean', methods=['POST'])
def state_mean_request():

    if "question" not in request.json:
        return error_response(NO_QUESTION_REASON)
    
    if "state" not in request.json:
        return error_response(NO_STATE_REASON)

    try:
        id = current_app.query_handler.handle_query("state_mean", request.json)
    except HandlerTerminatedException:
        return error_response(HANDLER_TERMINATED_EXCEPTION)

    return job_id_response(id)

@queries_blueprint.route('/api/worst5', methods=['POST'])
def worst5_request():

    if "question" not in request.json:
        return error_response(NO_QUESTION_REASON)

    try:
        id = current_app.query_handler.handle_query("worst5", request.json)
    except HandlerTerminatedException:
        return error_response(HANDLER_TERMINATED_EXCEPTION)

    return job_id_response(id)

@queries_blueprint.route('/api/global_mean', methods=['POST'])
def global_mean_request():

    if "question" not in request.json:
        return error_response(NO_QUESTION_REASON)

    try:
        id = current_app.query_handler.handle_query("global_mean", request.json)
    except HandlerTerminatedException:
        return error_response(HANDLER_TERMINATED_EXCEPTION)

    return job_id_response(id)

@queries_blueprint.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():

    if "question" not in request.json:
        return error_response(NO_QUESTION_REASON)

    try:
        id = current_app.query_handler.handle_query("diff_from_mean", request.json)
    except HandlerTerminatedException:
        return error_response(HANDLER_TERMINATED_EXCEPTION)

    return job_id_response(id)

@queries_blueprint.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():

    if "question" not in request.json:
        return error_response(NO_QUESTION_REASON)
    
    if "state" not in request.json:
        return error_response(NO_STATE_REASON)

    try:
        id = current_app.query_handler.handle_query("state_diff_from_mean", request.json)
    except HandlerTerminatedException:
        return error_response(HANDLER_TERMINATED_EXCEPTION)

    return job_id_response(id)

@queries_blueprint.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():

    if "question" not in request.json:
        return error_response(NO_QUESTION_REASON)

    try:
        id = current_app.query_handler.handle_query("mean_by_category", request.json)
    except HandlerTerminatedException:
        return error_response(HANDLER_TERMINATED_EXCEPTION)

    return job_id_response(id)

@queries_blueprint.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():

    if "question" not in request.json:
        return error_response(NO_QUESTION_REASON)
    
    if "state" not in request.json:
        return error_response(NO_STATE_REASON)

    try:
        id = current_app.query_handler.handle_query("state_mean_by_category", request.json)
    except HandlerTerminatedException:
        return error_response(HANDLER_TERMINATED_EXCEPTION)

    return job_id_response(id)
