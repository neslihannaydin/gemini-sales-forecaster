from forecasting.forecast_sales import forecast_sales
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")

def extract_forecast_params(query: str) -> dict:
    prompt = f"""
Sen bir satış tahmini asistanısın. Kullanıcının sorusunu okuyup şu parametreleri JSON formatında çıkart:

- category (toys, clothing, groceries, furniture, electronics)
- month_offset (kaç ay sonrası)
- price (float)
- competitor_price (float)
- inventory (int)
- region (North, South, East, West)

Sadece geçerli JSON verisi döndür. Açıklama yazma.

Soru: "{query}"
"""
    response = model.generate_content(prompt)
    cleaned = response.text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(cleaned)

def chatbot_loop():
    print("🤖 Tahmin Botu'na hoş geldin. Çıkmak için 'çık' yaz 💬\n")
    while True:
        user_input = input("👤 Sen: ")
        if user_input.lower() in ["çık", "exit", "quit"]:
            print("👋 Güle güle bebişim!")
            break

        try:
            parsed = extract_forecast_params(user_input)
            result = forecast_sales(
                category=parsed["category"],
                month_offset=parsed["month_offset"],
                price=parsed["price"],
                competitor_price=parsed["competitor_price"],
                inventory=parsed["inventory"],
                region=parsed["region"]
            )
            print(f"🤖 Tahmin Edilen Satış: {result} adet\n")
        except Exception as e:
            print("❌ Anlayamadım efendim, tekrar deneyebilir misiniz?\n")
            print("🔧 Hata:", e)

if __name__ == "__main__":
    chatbot_loop()
