import pandas as pd

def load_and_prepare_data(path="sales_data.csv"):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Weekday"] = df["Date"].dt.weekday

    # Gereksiz sütunları çıkar
    df = df.drop(columns=["Store ID", "Product ID", "Demand", "Date"])

    # Kategorik sütunlar
    cat_cols = ["Category", "Region", "Weather Condition", "Promotion", "Seasonality", "Epidemic"]
    df = pd.get_dummies(df, columns=cat_cols, drop_first=False)
    
    return df
