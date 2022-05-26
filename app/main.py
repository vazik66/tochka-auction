from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import fastapi_jsonrpc
from app.api.api_v1.payment import rpc


def get_application():
    _app = fastapi_jsonrpc.API(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["POST"],
        allow_headers=["*"],
    )
    return _app


if __name__ == "__main__":
    import uvicorn

    app = get_application()
    app.bind_entrypoint(rpc)
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
