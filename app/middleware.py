import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Setting up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom middleware for logging
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request details
        request_body = await request.body()
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Request body: {request_body.decode('utf-8') if request_body else 'No body'}")

        # Process the request
        response = await call_next(request)

        # Read and log response body
        response_body = [section async for section in response.body_iterator]
        response_text = b"".join(response_body).decode("utf-8")

        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response body: {response_text}")

        # Return the response correctly
        return Response(content=response_text, status_code=response.status_code, headers=dict(response.headers))
