def api_response(status_code=200, data=None, error=None, message=None):
    response = {"status_code": status_code}
    if data is not None:
        response["data"] = data
    if error is not None:
        response["error"] = error
    if message is not None:
        response["message"] = message
    return response
