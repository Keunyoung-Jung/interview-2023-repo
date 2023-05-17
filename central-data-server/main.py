import os

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.params import Path
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

from central import settings
from central.constants import BASE_DIR
from central.models import Admin
from central.providers import LoginProvider
from fastapi_admin.app import app as admin_app
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
    unauthorized_error_exception,
)
from central.api import model_router
from central.api import dictionary_router
from central.api import analyzer_router
from central.api import download_router

def create_app():
    app = FastAPI(title=f'Data Team API')
    app.mount(
        "/admin/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "static")),
        name="static",
    )

    @app.get("/")
    async def index():
        return RedirectResponse(url="/admin")

    admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
    admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
    admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
    admin_app.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)

    @app.on_event("startup")
    async def startup():
        r = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            encoding="utf8",
        )
        await admin_app.configure(
            logo_url="assets/horizontal-logo.412b0cbf.svg",
            template_folders=[os.path.join(BASE_DIR, "templates")],
            favicon_url="favicon.png",
            providers=[
                LoginProvider(
                    login_logo_url="favicon.png",
                    admin_model=Admin,
                )
            ],
            redis=r,
        )

    app.mount("/admin", admin_app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    register_tortoise(
        app,
        config={
            "connections": {"default": settings.DATABASE_URL},
            "apps": {
                "models": {
                    "models": ["central.models"],
                    "default_connection": "default",
                }
            },
        },
        generate_schemas=True,
    )
    return app


app_ = create_app()
app_.include_router(model_router)
app_.include_router(analyzer_router)
app_.include_router(download_router)
app_.include_router(dictionary_router)

if __name__ == "__main__":
    uvicorn.run("main:app_", debug=True, reload=True)
