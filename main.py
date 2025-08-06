from forecasting.forecast_sales import forecast_sales
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# .env içinden API anahtarı al
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-pro")

def ask_user_query(query: str):
    prompt = f"""
Sen bir satış tahmin yardımcısısın. Kullanıcıdan bir cümle alacaksın ve bu cümlede aşağıdaki bilgileri çıkartacaksın:
- category (toys, clothing, groceries, furniture, electronics)
- month_offset (kaç ay sonrası?)
- price (ürün fiyatı)
- competitor_price (rakip fiyatı)
- inventory (stok sayısı)
- region (North, South, East, West gibi)

Eğer bilgi yoksa tahmini yapma, uyarı döndür. 
Yanıtı sadece JSON formatında ver:

"{query}"
"""

    response = model.generate_content(prompt)
    return response.text



if __name__ == "__main__":
    query = input("💬 Bir şey sor (örnek: 3 ay sonra toys satış tahmini):\n")
    #response = ask_user_query(query)
    json_text = ask_user_query(query)

    try:
        cleaned = json_text.strip().removeprefix("```json").removesuffix("```").strip()
        parsed = json.loads(cleaned)
        result = forecast_sales(
            category=parsed["category"],
            month_offset=parsed["month_offset"],
            price=parsed["price"],
            competitor_price=parsed["competitor_price"],
            inventory=parsed["inventory"],
            region=parsed["region"]
        )
        print(f"\n📦 Tahmin Edilen Satış (toplam): {result} adet")
    except Exception as e:
        print("❌ Tahmin yapılamadı:", e)
        print("Gemini cevabı:", json_text)