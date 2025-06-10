from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging_config import logger
import time


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = round(time.time() - start_time, 4)

        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} in {process_time}s"
        )
        return response
