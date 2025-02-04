import enum
from datetime import datetime
from os import getenv

from sqlalchemy import DECIMAL, ForeignKey, Column, Enum, DateTime, Text
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, Session, SQLModel, create_engine, select, VARCHAR, TEXT, Relationship
from dotenv import load_dotenv
load_dotenv()

class BaseSQLModel(SQLModel , abstract=True):
    id: int | None = Field(primary_key=True)
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class User(BaseSQLModel, table=True):
    name: str
    email : str = Field(unique=True)
    username : str = Field(unique=True)
    password : str = Field(min_length=5)
    expenses : list['Expense'] = Relationship(back_populates='user' , cascade_delete=True)



class TypeEnum(str , enum.Enum):
    INCOME = 'income'
    EXPENSE = 'expense'

class Category(BaseSQLModel , table=True):

    __tablename__ = "categories"
    name: str = Field(VARCHAR(255))
    type : TypeEnum = Field(sa_column=Column(Enum(TypeEnum,values_callable=lambda x: [i.value for i in x])))
    icon : str
    expenses : list['Expense'] = Relationship(back_populates='category' , cascade_delete=True)

class Expense(BaseSQLModel , table = True):
    type : TypeEnum = Field(sa_column=Column(Enum(TypeEnum,values_callable=lambda x: [i.value for i in x])))
    category_id : int = Field(foreign_key='categories.id')
    category : 'Category' = Relationship(back_populates='expenses')
    user_id : int = Field(foreign_key='users.id')
    user : 'User' = Relationship(back_populates='expenses')
    amount : float = Field(DECIMAL(8,0))
    description : str = Field(Text)
    created_at : datetime = Field(default_factory=datetime.now , nullable=False)


DB_NAME=getenv('DB_NAME')
DB_USER=getenv('DB_USER')
DB_HOST=getenv('DB_HOST')
DB_PORT=getenv('DB_PORT')
DB_PASSWORD=getenv('DB_PASSWORD')

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SQLModel.metadata.create_all(engine)

