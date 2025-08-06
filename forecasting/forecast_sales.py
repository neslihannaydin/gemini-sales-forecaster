import pandas as pd
import joblib
from datetime import datetime, timedelta

def forecast_sales(category: str, month_offset: int,
                   price: float, competitor_price: float,
                   inventory: int, region: str = "North") -> int:
    
    model_path = f"models/{category.lower()}_model.pkl"
    model = joblib.load(model_path)
    needed_cols = model.feature_names_in_

    today = datetime.today()
    year = today.year + ((today.month + month_offset - 1) // 12)
    month = ((today.month + month_offset - 1) % 12) + 1
    start_date = datetime(year, month, 1)

    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)

    rows = []
    curr = start_date
    while curr <= end_date:
        row = {
            "Inventory Level": inventory,
            "Price": price,
            "Competitor Pricing": competitor_price,
            "Month": curr.month,
            "Day": curr.day,
            "Weekday": curr.weekday(),
            f"Category_{category.title()}": 1,
            f"Region_{region.title()}": 1,
            "Epidemic_None": 1
        }
        rows.append(row)
        curr += timedelta(days=1)

    df = pd.DataFrame(rows)

    # Eksik sütunları 0 ile doldur
    for col in needed_cols:
        if col not in df.columns:
            df[col] = 0
    df = df[needed_cols]

    preds = model.predict(df)
    return round(preds.sum())
