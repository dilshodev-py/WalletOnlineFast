from typing import Annotated

from fastapi import FastAPI, Request, Depends
from sqlmodel import Session, select
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.models import engine, Expense, Category

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@app.get('/income/form')
async def income_form(request:Request , session : SessionDep ):
    print(request)
    categories = session.exec(select(Category).where(Category.type=='income')).fetchall()
    return templates.TemplateResponse(request , 'income.html',{'categories':categories})




# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
