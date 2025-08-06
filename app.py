import streamlit as st
from forecasting.forecast_sales import forecast_sales
from chatbot import model  # Gemini modelini içe aktar

st.set_page_config(page_title="Satış Tahmin Aracı", page_icon="📦")

# --- Anahtar Kelime Çıkarımı ---
def extract_tags(text: str) -> list:
    prompt = f"""
    Kullanıcının mesajından 3-5 tane anahtar kelime çıkar. Virgülle ayır ve sadece kelimeleri ver.
    Mesaj: "{text}"
    """
    response = model.generate_content(prompt)
    tags = response.text.strip().split(",")
    return [tag.strip().lower() for tag in tags if tag.strip()]

# --- STATE TANIMLARI ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = None


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

        # Tahmini ve girdileri session_state'e kaydet
        st.session_state.last_prediction = prediction
        st.session_state.last_inputs = {
            "category": category,
            "month_offset": month_offset,
            "price": price,
            "competitor_price": competitor_price,
            "inventory": inventory,
            "region": region
        }
    except Exception as e:
        st.error(f"❌ Tahmin yapılamadı: {e}")

# --- CHATBOT BÖLÜMÜ ---
st.info("👋 Merhaba! Ben satış danışmanınızım. Geçmiş veriler, stok bilgisi ve fiyatlara göre sana analiz yapabilirim. Tahmin aldıysan detaylarını sorabilir, almadıysan yine de bana danışabilirsin!")
st.subheader("🧠 Chatbot ile Sohbet Et")

def explain_forecast_with_llm(data: dict, user_question: str) -> str:
    prompt = f"""
    Aşağıdaki tahmin verilerine göre kullanıcıdan gelen soruyu anlamlı şekilde açıkla.

    📊 Veriler:
    - Kategori: {data['category']}
    - Ay: {data['month_offset']}
    - Ürün Fiyatı: {data['price']}
    - Rakip Fiyat: {data['competitor_price']}
    - Stok: {data['inventory']}
    - Bölge: {data['region']}
    - Tahmin Sonucu: {data['predicted_sales']}

    ❓ Soru: {user_question}

    Açıklamayı sadeleştirerek ve neden-sonuç ilişkisi kurarak yap.
    """
    response = model.generate_content(prompt)
    return response.text if response.parts else "❌ LLM cevap döndüremedi. Lütfen daha net sor."

# --- Sohbet Formu ---
with st.form("chat_form", clear_on_submit=True):
    user_question = st.text_area("Bir soru yazın...", height=50)
    send = st.form_submit_button("💬 Gönder")

if send and user_question.strip():
    if st.session_state.last_prediction is None:
        prompt = f"Kullanıcının sorusu: {user_question}\nLütfen satış tahminleri hakkında genel bir şekilde yardımcı ol."
        response = model.generate_content(prompt)
        response_text = response.text if response.parts else "❌ LLM cevap döndüremedi. Lütfen daha açık bir soru yazın."
    else:
        data = st.session_state.last_inputs.copy()
        data["predicted_sales"] = st.session_state.last_prediction
        response_text = explain_forecast_with_llm(data, user_question)

    # Tag çıkarımı ve geçmişe kayıt
    tags = extract_tags(user_question)
    st.session_state.chat_history.append({
        "user": user_question,
        "bot": response_text,
        "tags": tags
    })

# --- Chat Geçmişi: Scrollable + Filtrelenebilir ---
st.markdown("### 🧾 Sohbet Geçmişi")

# 🔎 Filtreleme alanı
all_tags = set()
for chat in st.session_state.chat_history:
    all_tags.update(chat.get("tags", []))

selected_tags = st.multiselect("🗂 Sohbet geçmişini filtrele", sorted(all_tags))

if selected_tags:
    filtered_chats = [
        chat for chat in st.session_state.chat_history
        if any(tag in chat.get("tags", []) for tag in selected_tags)
    ]
else:
    filtered_chats = st.session_state.chat_history

# --- Stil (scrollable container) ---
chat_container_css = """
<style>
.scrollable-chat {
    max-height: 400px;
    overflow-y: auto;
    padding: 1rem;
    border: 1px solid #444;
    border-radius: 10px;
    background-color: #111111;
}
.scrollable-chat::-webkit-scrollbar {
    width: 6px;
}
.scrollable-chat::-webkit-scrollbar-thumb {
    background-color: #666;
    border-radius: 5px;
}
.scrollable-chat::-webkit-scrollbar-track {
    background-color: #222;
}
</style>
"""
st.markdown(chat_container_css, unsafe_allow_html=True)
st.markdown('<div class="scrollable-chat">', unsafe_allow_html=True)

# Sohbeti yeni üstte olacak şekilde sırala
for chat in reversed(filtered_chats):
    with st.chat_message("user"):
        st.markdown(f"""
        <div style="
            max-height: 150px;
            overflow-y: auto;
            padding: 0.5rem;
            background-color: #1e1e1e;
            border-radius: 8px;
            border: 1px solid #444;
            font-size: 0.95rem;">
            {chat['user']}
        </div>
        """, unsafe_allow_html=True)
    with st.chat_message("assistant"):
        st.markdown(f"""
        <div style="
            max-height: 150px;
            overflow-y: auto;
            padding: 0.5rem;
            background-color: #222;
            border-radius: 8px;
            border: 1px solid #555;
            font-size: 0.95rem;">
            {chat['bot']}
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)