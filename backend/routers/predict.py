from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import RemittanceFlow
from ml.forecast import predict_remittance

router = APIRouter(prefix="/predict", tags=["predict"])

@router.get("/")
def get_prediction(
    years: int = Query(default=3, ge=1, le=10),
    db: Session = Depends(get_db)
):
    results = db.query(
        RemittanceFlow.year_ad,
        func.sum(RemittanceFlow.amount_usd).label("total_amount_usd")
    ).group_by(
        RemittanceFlow.year_ad
    ).order_by(RemittanceFlow.year_ad).all()

    historical = [
        {"year_ad": r.year_ad, "total_amount_usd": r.total_amount_usd}
        for r in results
    ]

    forecast = predict_remittance(historical, years)

    return {
        "historical": historical,
        "forecast": forecast
    }