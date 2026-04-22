import numpy as np
from sklearn.linear_model import LinearRegression

def predict_remittance(historical_data: list[dict], years_ahead: int) -> list[dict]:
    """
    historical_data: list of {"year_ad": int, "total_amount_usd": float}
    returns: list of {"year_ad": int, "predicted_amount_usd": float}
    """
    X = np.array([d["year_ad"] for d in historical_data]).reshape(-1, 1)
    y = np.array([d["total_amount_usd"] for d in historical_data])

    model = LinearRegression()
    model.fit(X, y)

    last_year = max(d["year_ad"] for d in historical_data)
    future_years = [last_year + i for i in range(1, years_ahead + 1)]
    X_future = np.array(future_years).reshape(-1, 1)
    predictions = model.predict(X_future)

    return [
        {
            "year_ad": int(year),
            "predicted_amount_usd": round(float(pred), 2)
        }
        for year, pred in zip(future_years, predictions)
    ]