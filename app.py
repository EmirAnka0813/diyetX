"""
DiyetX - AI Destekli Diyet Uygulaması
Streamlit Uygulaması
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Sentry entegrasyonu (hata izleme)
import sentry_sdk

sentry_sdk.init(
    dsn="https://97f83997b663a5a3545311ee0582c716@o4511259385397248.ingest.us.sentry.io/4511281486626816",
    traces_sample_rate=1.0,
)

st.set_page_config(page_title="DiyetX", page_icon="🥗", layout="wide")

# Sayfa başlığı
st.title("🥗 DiyetX - AI Destekli Diyet Asistanı")
st.markdown("**Sağlıklı beslen, hedefine ulaş!**")

# Sidebar menüsü
st.sidebar.title("📋 Menü")
menu = st.sidebar.radio(
    "Ne yapmak istiyorsun?",
    ["🏠 Ana Sayfa", "🍽️ Kalori Takibi", "📊 İlerleme", "💬 AI Danışman", "⚙️ Ayarlar"]
)

# Ana Sayfa
if menu == "🏠 Ana Sayfa":
    st.header("Hoş Geldin!")
    
    # Kullanıcı bilgileri (simüle)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📅 Gün", "Bugün")
    with col2:
        st.metric("🔥 Kalori Hedefi", "2000 kcal")
    with col3:
        st.metric("💧 Su", "5/8 bardak")
    
    st.markdown("---")
    
    # Hızlı giriş
    st.subheader("🍽️ Yemek Ekle")
    
    yemek_adi = st.text_input("Yemek adı")
    kalori = st.number_input("Kalori", min_value=0, max_value=2000, value=0)
    
    if st.button("Ekle ✅"):
        if yemek_adi:
            st.success(f"{yemek_adi} eklendi! ({kalori} kcal)")
        else:
            st.warning("Lütfen yemek adı gir!")
    
    # Önerilen yemekler
    st.markdown("### 🥗 Popüler Yemekler")
    yemekler = pd.DataFrame({
        "Yemek": ["Tavuk Salatası", "Yoğurt", "Meyve", "Fıstık Ezmesi"],
        "Kalori": [350, 150, 80, 200],
        "Protein": ["30g", "15g", "1g", "7g"]
    })
    st.dataframe(yemekler, use_container_width=True)

# Kalori Takibi
elif menu == "🍽️ Kalori Takibi":
    st.header("📝 Günlük Kalori Takibi")
    
    tarih = st.date_input("Tarih seç", datetime.now())
    
    # Yemek listesi (simüle)
    yemekler_gunluk = pd.DataFrame({
        "Saat": ["08:00", "12:30", "15:00", "19:00"],
        "Yemek": ["Kahvaltı (Yulaf)", "Öğle (Tavuk)", "Atıştırmalık (Meyve)", "Akşam (Balık)"],
        "Kalori": [350, 550, 150, 450]
    })
    
    st.dataframe(yemekler_gunluk, use_container_width=True)
    
    toplam_kalori = yemekler_gunluk["Kalori"].sum()
    st.metric("Toplam Kalori", f"{toplam_kalori} kcal")
    
    # Progress bar
    progress = min(toplam_kalori / 2000, 1.0)
    st.progress(progress, text=f"Günlük hedefe {int(progress*100)}% ulaşıldı")

# İlerleme
elif menu == "📊 İlerleme":
    st.header("📈 İlerleme Grafikleri")
    
    # Haftalık veriler (simüle)
    haftalar = ["1. Hafta", "2. Hafta", "3. Hafta", "4. Hafta"]
    kilolar = [85, 84, 83, 82]
    
    chart_data = pd.DataFrame({"Hafta": haftalar, "Kilo (kg)": kilolar})
    st.line_chart(chart_data.set_index("Hafta"))
    
    st.metric("Toplam Kilo Kaybı", "-3 kg")

# AI Danışman
elif menu == "💬 AI Danışman":
    st.header("🤖 AI Diyet Danışmanı")
    
    st.markdown("Soru sor, sana yardımcı olayım!")
    
    soru = st.text_area("Bir soru sor:", placeholder="Örnek: Bugün ne yemeliyim?")
    
    if st.button("Sor 📩"):
        if soru:
            with st.spinner("AI düşünüyor..."):
                # Simüle edilmiş yanıt
                cevap = f"""Bugünün menusu için önerim:
                
🍳 **Kahvaltı:** Yulaf ezmesi + meyve
🥗 **Öğle:** Izgara tavuk + salata
🍎 **Ara:** Bir avuç badem
🐟 **Akşam:** Fırında somon + sebze

**Toplam:** ~1800 kcal
**Protein:** Yüksek
**Karbonhidrat:** Orta"""

                st.success(cevap)
        else:
            st.warning("Lütfen bir soru yaz!")
    
    st.markdown("---")
    st.markdown("**Veya sesli sor:** 🎤 (Yakında!)")

# Ayarlar
elif menu == "⚙️ Ayarlar":
    st.header("⚙️ Ayarlar")
    
    # Profil ayarları
    st.subheader("👤 Profil")
    yas = st.number_input("Yaş", min_value=10, max_value=80, value=15)
    kilo = st.number_input("Kilo (kg)", min_value=30, max_value=200, value=82)
    boy = st.number_input("Boy (cm)", min_value=100, max_value=220, value=170)
    
    hedef_kilo = st.number_input("Hedef Kilo (kg)", min_value=30, max_value=200, value=75)
    
    if st.button("Kaydet 💾"):
        st.success("Ayarlar kaydedildi!")
    
    st.markdown("---")
    
    # Bildirimler
    st.subheader("🔔 Bildirimler")
    hatirlatma = st.toggle("Günlük hatırlatma", value=True)
    su_hatirlatma = st.toggle("Su içme hatırlatması", value=True)
    
    st.markdown("---")
    st.markdown("**DiyetX v0.1** - Beta sürüm")

st.markdown("---")
st.caption("© 2026 DiyetX - Tüm hakları saklıdır.")