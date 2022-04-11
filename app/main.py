from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import fastapi_jsonrpc
from app.api.api_v1.items import rpc


def get_application():
    _app = fastapi_jsonrpc.API(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


app = get_application()
app.bind_entrypoint(rpc)
