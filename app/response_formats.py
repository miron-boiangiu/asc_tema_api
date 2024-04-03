"""
General methods and strings for formatting responses.
"""


NO_QUESTION_REASON = "The request must include a question."
NO_STATE_REASON = "The request must include a state."
INVALID_JOB_ID_REASON = "Invalid job_id"
HANDLER_TERMINATED_EXCEPTION = "The query handler has been terminated. " + \
                                "No new requests can be handled."

def job_id_response(id):
    """
    Job id response format.
    """

    return {
        "job_id": f"job_id_{id}"
    }

def error_response(reason=""):
    """
    Error response format.
    """

    msg = {
        "status": "error",
    }

    if reason:
        msg["reason"] = reason

    return msg

def running_response():
    """
    Still running query response format.
    """

    return {
        "status": "running",
    }

def data_response(data):
    """
    Data response format.
    """

    return {
        "status": "done",
        "data": data
    }
