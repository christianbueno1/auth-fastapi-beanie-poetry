from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
# Set the templates directory relative to your working dir
templates = Jinja2Templates(directory="auth_fastapi_beanie_poetry/templates")

@router.get("/test-reset", response_class=HTMLResponse)
async def test_reset(request: Request):
    context = {
        "request": request,
        "reset_link": "https://example.com/reset?token=testtoken",
        "username": "TestUser",
        # "contact_support": "mailto:support@example.com"
        "contact_support": "www.ricospice.store/contact",
        "domain": "www.ricospice.store",
        "href_domain": "https://www.ricospice.store",
    }
    return templates.TemplateResponse("reset_password.html", context)