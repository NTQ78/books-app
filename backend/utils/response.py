from typing import Any
from fastapi import status as http_status

from fastapi.responses import JSONResponse
from fastapi import HTTPException


def api_response(status_code=200, data=None, error=None, message=None):
    return {
        "status_code": status_code,
        "data": data,
        "error": error,
        "message": message,
    }
