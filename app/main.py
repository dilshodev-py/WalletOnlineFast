from fastapi import FastAPI, Request
from sqlmodel import Session, select
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.models import engine, Expense, Category

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get('/income/form')
async def income_form(request:Request):
    with Session(engine) as session:
        categories = session.exec(select(Category)).all()
        return templates.TemplateResponse('income.html',{'request':request,'categories':categories})




# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
