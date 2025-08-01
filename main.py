from fastapi import FastAPI
from render import build_invite
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from render import build_invite
from fastapi import Body
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        "homepage.html",
        {"request": request}
    )

@app.get("/create-form")
def create_form(request: Request):
    return templates.TemplateResponse(
        request,
        "form.html",
        {}
    )

@app.post("/generate-invites")
async def generate_invites(payload: dict = Body(...)):
    try:
        build_invite(payload)
        zip_path = "invites/invite_all.zip"
        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename="thu_moi_phu_huynh.zip",
            headers={
                "Content-Disposition": "attachment; filename=thu_moi_phu_huynh.zip"
            }
        )
    except Exception as e:
        return JSONResponse({
            "message": f"❌ Lỗi tạo thư mời: {str(e)}",
            "status": "error"
        }, status_code=500)