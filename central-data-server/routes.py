from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_404_NOT_FOUND

from central.models import Config
from fastapi_admin.app import app
from fastapi_admin.depends import get_resources
from fastapi_admin.depends import get_current_admin
from fastapi_admin.template import templates


@app.get("/")
async def home(
    request: Request,
    resources=Depends(get_resources),
):
    if not request.state.admin :
        return RedirectResponse(url="/admin/login")
    else :
        return templates.TemplateResponse(
            "dashboard.html",
            context={
                "request": request,
                "resources": resources,
                "resource_label": "Dashboard",
                "page_pre_title": "overview",
                "page_title": "Dashboard",
            },
        )
        
@app.get("/guide")
async def guide(
    request: Request,
    resources=Depends(get_resources),
):
    if not request.state.admin :
        return RedirectResponse(url="/admin/login")
    else :
        return templates.TemplateResponse(
            "guide.html",
            context={
                "request": request,
                "resources": resources,
                "resource_label": "가이드 문서",
                "page_pre_title": "가이드 문서",
                "page_title": "가이드 문서",
            },
        )

@app.put("/config/switch_status/{config_id}")
async def switch_config_status(request: Request, config_id: int):
    config = await Config.get_or_none(pk=config_id)
    if not config:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    config.status = not config.status
    await config.save(update_fields=["status"])
    return RedirectResponse(url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER)
