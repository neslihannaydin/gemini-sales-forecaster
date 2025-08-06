# 📦 Sales Forecaster with Gemini-LLM Support

Bu proje, e-ticaret ürünleri için **kategori bazlı satış tahmini** yapan ve tahmin sonuçlarını **doğal dilde açıklayan** bir yapay zekâ destekli satış danışmanı sistemidir.  
Streamlit arayüzü üzerinden kullanıcılar, geçmiş verilerle tahmin alabilir ve sonrasında sorularını Gemini destekli chatbot’a sorabilir.  
Veri seti, [Kaggle](https://www.kaggle.com/) üzerinden alınmıştır ve 5 farklı ürün kategorisine ait tarihsel satış, stok, fiyat ve bölgesel bilgilerden oluşmaktadır.

---

## 🚀 Özellikler

- 🔢 Random Forest ile **kategoriye özel satış tahmini** (`toys`, `furniture`, `clothing`, `electronics`, `groceries`)
- 🤖 Google Gemini destekli **LLM tabanlı chatbot**
- 🔍 Kullanıcı sorularından **otomatik kelime (tag) çıkarımı**
- 🗂️ Sohbet geçmişini **etikete göre filtreleme**
- 💬 Scrollable ve kullanıcı dostu **soru-cevap arayüzü**
- 🧠 Gerçek verilerle zenginleştirilmiş doğal dil açıklamalar

---

## 🧱 Proje Yapısı

```

├── app.py # Streamlit arayüzü
├── chatbot.py # Gemini LLM entegrasyonu
├── main.py
├── forecasting/
│ └── forecast_sales.py # Tahmin fonksiyonu
├── train_models/
│ ├── train_model.py # RF modeli eğitimi
│ └── run_all.py # Tüm modelleri topluca eğitir
├── models/ # Eğitilen .pkl dosyaları (5 kategori)
├── utils/
│ ├── preprocessing.py # Veri işleme fonksiyonları
│ └── plotting.py # (İsteğe bağlı) grafik çizimleri
├── data/
│ └── sales_data.csv # Eğitim/test verisi
├── .env # API anahtarı gibi gizli bilgiler
├── requirements.txt # Gerekli kütüphaneler
├── .gitignore

```


## ⚙ Kurulum

### 1. Sanal Ortam Oluşturma (Opsiyonel) ve Bağımlılıkların Yüklenmesi

```
bash
python -m venv venv

# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

### 2. .env Dosyasını Oluştur

Proje kök dizininde .env dosyası oluşturun ve içine aşağıdaki satırı ekleyin:

```
GEMINI_API_KEY=senin_api_keyin_buraya
```

### 3. Modeli Eğit ve Uygulamayı Başlat
```
bash
python run_all.py
streamlit run app.py
```

---

## 💡 Nasıl Çalışır?

- Kullanıcı ürün kategorisi ve satış parametrelerini girer, ardından *"Tahmin Et"* butonuna basar.
- Sistem forecast_sales() fonksiyonuyla Random Forest modelinden tahmin sonucu döner.
- Tahmin sonrası kullanıcı soru sorabilir, chatbot devreye girer.
- Gemini modeli tahmin verisi ve kullanıcı sorusunu analiz edip anlamlı açıklamalar üretir.
- Soru içerisinden 3–5 adet anahtar kelime (tag) çıkarılır.
- Sohbet geçmişi bu tag’lere göre filtrelenerek gösterilebilir.

---

## 🧠 Kullanılan Teknolojiler

- Python
- Streamlit
- Google Gemini API
- Random Forest (Scikit-learn)
- Pandas, NumPy

---

## 🧾 Tag Tabanlı Sohbet Geçmişi

Chatbot geçmişi aşağıdaki formatta JSON olarak saklanır:
```
json
{
  "user": "Stok yeterli mi?",
  "bot": "Tahmini talep 379 adet...",
  "tags": ["stok", "talep", "adet"]
}
```

Arayüzdeki filtre kutusu sayesinde, geçmiş konuşmalar tag’lere göre dinamik şekilde listelenebilir.

---

## 📜 Lisans & Notlar

- Proje, BTK Akademi x Google x Girişimcilik Vakfı iş birliği ile AI Hackathon yarışması için hazırlanmıştır.
- Tahminler sadece mevcut veri setine dayalıdır; gerçek zamanlı veri veya harici kaynaklar kullanılmaz.
