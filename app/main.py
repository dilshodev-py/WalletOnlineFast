from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import func, sum
from sqlmodel import SQLModel, Session, select
from starlette.requests import Request  # Request import qilish
from starlette.templating import Jinja2Templates

from app.models import engine, Expense  # Agar Category ham kerak bo'lsa, uni import qilish

app = FastAPI()

templates = Jinja2Templates(directory="templates")

SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session


# Asosiy endpoint
@app.get("/", response_class=HTMLResponse)
async def expanse(request: Request, session: Session = Depends(get_session)):
    expenses = session.exec(select(Expense)).all()
    income = session.exec(func.sum(Expense.amount)).fil(Expense.type == 'income').one_or_none()
    return templates.TemplateResponse("home-page.html", {"request": request, "expenses": expenses, "income": income})
