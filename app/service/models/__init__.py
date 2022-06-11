import datetime

from pydantic import BaseModel


class PostalCode(BaseModel):
    code: str
    the_geom: str


class PaystatAggregation(BaseModel):
    p_gender: str
    p_age: str
    amount: float
    code: str | None
    p_month: datetime.date | None
