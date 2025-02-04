from typing import Annotated

from fastapi import FastAPI, Request, Depends
from sqlalchemy import func
from sqlmodel import Session, select
from starlette.responses import HTMLResponse
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



# Asosiy endpoint
@app.get("/", response_class=HTMLResponse)
async def expanse(request: Request, session: Session = Depends(get_session)):
    expenses = session.exec(select(Expense)).all()
    income = session.exec(func.sum(Expense.amount)).where(Expense.type == 'income').one_or_none()
    return templates.TemplateResponse("home-page.html", {"request": request, "expenses": expenses, "income": income})
