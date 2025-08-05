import streamlit as st
from forecasting.forecast_sales import forecast_sales
from chatbot import model  # Gemini modelini içe aktar

st.set_page_config(page_title="Satış Tahmin Aracı", page_icon="📦")

st.title("📦 Satış Tahmin Aracı")

# --- GİRİŞ ALANLARI ---
category = st.selectbox("Kategori", ["toys", "furniture", "clothing", "electronics", "groceries"])
month_offset = st.slider("Kaç ay sonrası tahmin edilsin?", 1, 12, 3)
price = st.number_input("Ürün Fiyatı", min_value=0.0, format="%.2f")
competitor_price = st.number_input("Rakip Fiyatı", min_value=0.0, format="%.2f")
inventory = st.number_input("Stok Miktarı", min_value=0)
region = st.selectbox("Bölge", ["North", "South", "East", "West"])

# --- TAHMİN BUTONU ---
if st.button("🔮 Tahmin Et"):
    try:
        prediction = forecast_sales(
            category=category,
            month_offset=month_offset,
            price=price,
            competitor_price=competitor_price,
            inventory=inventory,
            region=region
        )
        st.success(f"🎯 Tahmin Edilen Satış (toplam): {prediction:.0f} adet")
    except Exception as e:
        st.error(f"❌ Tahmin yapılamadı: {e}")

st.markdown("---")

# --- LLM'E SORU ALANI ---
st.subheader("💬 Herhangi bir sorunuz varsa Gemini hazır! ")

user_question = st.text_input("Sorunuzu buraya yazın (örn: Bu kadar satış tahmini normal mi?)")

if st.button("🤖 LLM'e Sor") and user_question.strip() != "":
    prompt = f"""
    Aşağıdaki e-ticaret verilerine göre kullanıcıdan gelen soruyu yanıtla.

    📦 Veriler:
    - Kategori: {category}
    - Tahmin Edilen Ay: {month_offset}
    - Ürün Fiyatı: {price}
    - Rakip Fiyatı: {competitor_price}
    - Stok Miktarı: {inventory}
    - Bölge: {region}

    ❓ Soru: {user_question}

    Lütfen mantıklı ve kısa bir açıklama yap.
    """
    response = model.generate_content(prompt)

    if response.parts:
        st.markdown("#### 🧠 LLM Yanıtı:")
        st.write(response.text)
    else:
        st.error("❌ LLM cevap döndüremedi. Cevap boş geldi.")
