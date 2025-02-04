from pydantic import BaseModel


class IncomeForm(BaseModel):
    price : int
    description : str
    category : str
