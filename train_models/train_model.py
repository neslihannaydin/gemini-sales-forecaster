import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

from utils.preprocessing import load_and_prepare_data
from utils.plotting import plot_predictions


def train_category_model(category_name: str):
    print(f"\n📦 Kategori: {category_name.title()}")
    df = load_and_prepare_data()

    # Sütun adı kontrolü
    col_name = f"Category_{category_name.title()}"
    if col_name not in df.columns:
        print(f"❌ {col_name} sütunu bulunamadı.")
        return

    # Kategoriye ait satırları filtrele
    df_cat = df[df[col_name] == 1]
    if len(df_cat) < 50:
        print("❌ Yetersiz veri.")
        return

    # Hedef değişken
    y = df_cat["Units Sold"]

    # Ortak ve kategoriye özel çıkarılacak sütunlar
    common_excludes = ["Discount"]
    custom_excludes = {
        "toys": [
            "Seasonality_Summer", "Seasonality_Winter",
            "Promotion_Holiday"
        ],
        "furniture": [
            "Promotion_Holiday"
        ],
        "clothing": [
            # Seasonality önemli, çıkartılmıyor
        ],
        "electronics": [
            "Promotion_Holiday", "Seasonality_Winter"
        ],
        "groceries": [
            "Seasonality_Summer", "Promotion_Holiday"
        ]
}

    category_excludes = custom_excludes.get(category_name.lower(), [])
    dynamic_excludes = [
        col for col in df_cat.columns
        if col.startswith("Category_") or col.startswith("Promotion_") or col.startswith("Seasonality_")
    ]

    # Tüm çıkarılacak sütunlar
    all_excludes = list(set(common_excludes + category_excludes + dynamic_excludes))

    # Özellik matrisi (X)
    existing_excludes = [col for col in all_excludes if col in df_cat.columns]
    X = df_cat.drop(columns=["Units Sold"] + existing_excludes)

    # Eğitim/test bölmesi
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model oluştur ve eğit
    model = RandomForestRegressor(n_estimators=100, max_depth=6, min_samples_leaf=10, random_state=42)
    model.fit(X_train, y_train)

    # Değerlendirme
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"📉 MAE ({category_name.title()}): {mae:.2f}")

    # Görselleştirme + kayıt
    plot_predictions(y_test, y_pred, title=f"{category_name.title()} - Tahmin vs Gerçek")
    joblib.dump(model, f"models/{category_name.lower()}_model.pkl")
