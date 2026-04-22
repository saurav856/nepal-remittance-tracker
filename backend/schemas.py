from pydantic import BaseModel
from typing import Optional

class RemittanceFlowSchema(BaseModel):
    id: int
    fiscal_year: str
    year_ad: int
    source_country: str
    amount_usd: float
    num_workers: Optional[int]

    class Config:
        from_attributes = True

class SummarySchema(BaseModel):
    fiscal_year: str
    year_ad: int
    total_amount_usd: float
    total_workers: Optional[int]

class CountrySchema(BaseModel):
    source_country: str
    total_amount_usd: float
    total_workers: Optional[int]