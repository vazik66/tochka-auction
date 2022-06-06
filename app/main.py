from app.db.session import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import fastapi_jsonrpc
from app.api.api_v1.payment import rpc
from app.api.callback_handler.main import handler
from fastapi_utils.tasks import repeat_every
from app.crud.crud_item import end_auction, get_outdated_items


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
    app.mount("/payment", handler)

    # Create scheduled task to end outdated auctions
    # I should extract it somewhere but tomorrow will be math exam
    REPEAT_EVERY_IN_SECONDS = 60

    @app.on_event("startup")  # noqa
    @repeat_every(seconds=REPEAT_EVERY_IN_SECONDS)
    def end_outdated_auction() -> None:
        db = SessionLocal()
        outdated_items = get_outdated_items(db)
        for item in outdated_items:
            end_auction(db, item.id)

    uvicorn.run(
        app, host=settings.APP_HOST, port=settings.APP_PORT, proxy_headers=True
    )  # noqa
