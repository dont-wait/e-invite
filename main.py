from fastapi import FastAPI
from render import build_invite
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(
        request,
        "homepage.html",
        {}
    )

@app.get("/create-form")
def create_form(request: Request):
    return templates.TemplateResponse(
        request,
        "form.html",
        {}
    )