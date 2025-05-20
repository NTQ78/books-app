def api_response(status_code=200, data=None, error=None, message=None):
    return {
        "status_code": status_code,
        "data": data,
        "error": error,
        "message": message,
    }
