from flask import request, jsonify, Blueprint, current_app
from app.query_handler import NonexistentQueryException

import os
import json

queries_blueprint = Blueprint('queries', __name__)

@queries_blueprint.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    
    try:
        if current_app.query_handler.is_query_finished(job_id):
            return {
                  "status": "done",
                  "data": current_app.query_handler.get_query_result(job_id)
            }
        else:
            return {
                  "status": "running",
            }

    except NonexistentQueryException:
        return {
            "status": "error",
            "reason": "Invalid job_id",
        }

@queries_blueprint.route('/api/best5', methods=['POST'])
def best5_request():

    if "question" not in request.json:
        return {"status": "error",
                "reason": "The request must include a question."}

    id = current_app.query_handler.handle_query("best5", request.json)

    return {
        "job_id": f"job_id_{id}"
    }

@queries_blueprint.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    data = request.json
    print(f"Got request {data}")

    print(current_app.query_handler == None)

    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@queries_blueprint.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@queries_blueprint.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@queries_blueprint.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@queries_blueprint.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@queries_blueprint.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@queries_blueprint.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@queries_blueprint.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id


    return jsonify({"status": "NotImplemented"})
