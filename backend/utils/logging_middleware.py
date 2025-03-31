import logging
from fastapi import Request

async def log_requests(request: Request, call_next):
    logger = logging.getLogger("uvicorn")
    
    logger.debug(f"Request: {request.method} {request.url}")

    response = await call_next(request)

    logger.debug(f"Response Status: {response.status_code} for URL: {request.url}")

    return response
