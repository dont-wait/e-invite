from fastapi import FastAPI
from render import build_invite
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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