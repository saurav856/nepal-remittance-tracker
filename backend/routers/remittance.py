from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from database import get_db
from models import RemittanceFlow
from schemas import RemittanceFlowSchema, SummarySchema, CountrySchema

router = APIRouter(prefix="/remittance", tags=["remittance"])

@router.get("/", response_model=List[RemittanceFlowSchema])
def get_all(
    year: Optional[int] = Query(None),
    country: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(RemittanceFlow)
    if year:
        query = query.filter(RemittanceFlow.year_ad == year)
    if country:
        query = query.filter(RemittanceFlow.source_country == country)
    return query.all()

@router.get("/summary", response_model=List[SummarySchema])
def get_summary(db: Session = Depends(get_db)):
    results = db.query(
        RemittanceFlow.fiscal_year,
        RemittanceFlow.year_ad,
        func.sum(RemittanceFlow.amount_usd).label("total_amount_usd"),
        func.sum(RemittanceFlow.num_workers).label("total_workers")
    ).group_by(
        RemittanceFlow.fiscal_year,
        RemittanceFlow.year_ad
    ).order_by(RemittanceFlow.year_ad).all()

    return [
        SummarySchema(
            fiscal_year=r.fiscal_year,
            year_ad=r.year_ad,
            total_amount_usd=round(r.total_amount_usd, 2),
            total_workers=r.total_workers
        ) for r in results
    ]

@router.get("/by-country", response_model=List[CountrySchema])
def get_by_country(
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(
        RemittanceFlow.source_country,
        func.sum(RemittanceFlow.amount_usd).label("total_amount_usd"),
        func.sum(RemittanceFlow.num_workers).label("total_workers")
    )
    if year:
        query = query.filter(RemittanceFlow.year_ad == year)

    results = query.group_by(
        RemittanceFlow.source_country
    ).order_by(func.sum(RemittanceFlow.amount_usd).desc()).all()

    return [
        CountrySchema(
            source_country=r.source_country,
            total_amount_usd=round(r.total_amount_usd, 2),
            total_workers=r.total_workers
        ) for r in results
    ]