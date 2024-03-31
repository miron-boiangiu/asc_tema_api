NO_QUESTION_REASON = "The request must include a question."
NO_STATE_REASON = "The request must include a state."
INVALID_JOB_ID_REASON = "Invalid job_id"
HANDLER_TERMINATED_EXCEPTION = "The query handler has been terminated. No new requests can be handled."

def job_id_response(id):
    return {
        "job_id": f"job_id_{id}"
    }

def error_response(reason=""):

    msg = {
        "status": "error",
    }

    if reason:
        msg["reason"] = reason

    return msg

def running_response():
    return {
        "status": "running",
    }

def data_response(data):
    return {
        "status": "done",
        "data": data
    }
