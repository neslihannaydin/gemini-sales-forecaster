import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from utils.preprocessing import load_and_prepare_data
from utils.plotting import plot_predictions
import joblib

def run_model():
    print("\n🧸 Kategori: Toys")
    
    # 1. Veriyi hazırla
    df = load_and_prepare_data()

    # 2. Toys sütunu var mı kontrol et
    if "Category_Toys" not in df.columns:
        print("❌ 'Category_Toys' sütunu bulunamadı.")
        print("Mevcut kategoriler:", [col for col in df.columns if col.startswith("Category_")])
        return

    # 3. Toys satırlarını filtrele
    df_cat = df[df["Category_Toys"] == 1]
    print(f"🔢 Toys satır sayısı: {len(df_cat)}")

    if len(df_cat) < 50:
        print("❌ Yetersiz veri. Eğitim yapılmadı.")
        return

    # 4. Hedef ve özellikleri ayır
    y = df_cat["Units Sold"]

    # Çıkarılacak sütunlar: önemsiz + tüm Category sütunları
    cols_to_exclude = [
        "Discount"
    ] + [col for col in df_cat.columns if 
         col.startswith("Promotion_") or 
         col.startswith("Seasonality_") or 
         col.startswith("Category_")]

    X = df_cat.drop(columns=["Units Sold"] + cols_to_exclude)

    # 5. Eğitim ve test kümeleri
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 6. Modeli oluştur ve eğit (düzenlenmiş hiperparametreler)
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=6,
        min_samples_leaf=10,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 7. Tahmin ve değerlendirme
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"📉 MAE (Toys): {mae:.2f}")

    # 8. Görselleştir
    plot_predictions(y_test, y_pred, title="Category_Toys için Tahmin vs Gerçek (Tuned)")
    joblib.dump(model, "models/toys_model.pkl")