from typing import List, Optional

from pydantic import BaseModel

class CompanyBase(BaseModel):
    symbol: str
	name: str
	region: str
	marketOpen: str
	marketClose: str
	currency: str

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True


class PriceBase(BaseModel):
    open: float
    close: float
	high: float
	low: float
	volume: int
	period: str
	time: str

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    id: int
    company_id: int

    class Config:
        orm_mode = True