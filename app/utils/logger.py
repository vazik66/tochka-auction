from contextlib import asynccontextmanager
from fastapi_jsonrpc import JsonRpcContext
import logging
import os
from app.core.config import settings

if not os.path.exists(settings.LOGS_FOLDER):
    os.makedirs(settings.LOGS_FOLDER)


logging.basicConfig(
    filename=f"{settings.LOGS_FOLDER}/logs.txt",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s;%(levelname)s;%(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def logging_middleware(ctx: JsonRpcContext):
    logger.info("Request: %r", ctx.raw_request)
    try:
        yield
    finally:
        logger.info("Response: %r", ctx.raw_response)
