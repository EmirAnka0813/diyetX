"""
DiyetX - AI Destekli Diyet Uygulaması
Nutri ile Sesli Diyet Asistanı
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Sayfa ayarları
st.set_page_config(
    page_title="DiyetX",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS - Animasyonlu stil
st.markdown("""
<style>
    /* Ana tema */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Başlık */
    h1 {
        color: #00d4aa !important;
        text-align: center;
    }
    
    /* Kartlar */
    .metric-card {
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    /* Su butonu animasyonu */
    .water-button {
        background: linear-gradient(135deg, #00d4aa, #00b894);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 20px 40px;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,212,170,0.3);
    }
    
    .water-button:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(0,212,170,0.5);
    }
    
    .water-button:active {
        transform: scale(0.95);
    }
    
    /* Puan animasyonu */
    .points-pop {
        animation: pop 0.5s ease-out;
    }
    
    @keyframes pop {
        0% { transform: scale(0); opacity: 0; }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Nutri kutusu */
    .nutri-box {
        background: linear-gradient(135deg, #ff9a56, #ff6b35);
        border-radius: 25px;
        padding: 25px;
        color: white;
        font-size: 18px;
        margin: 20px 0;
        border: 3px solid #fff;
        box-shadow: 0 10px 40px rgba(255,107,53,0.3);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00d4aa, #00b894);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(255,255,255,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Session state başlat
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0

# Başlık
st.markdown("<h1>🥗 DiyetX</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#888;'>Nutri ile sağlıklı beslen, hedefine ulaş!</p>", unsafe_allow_html=True)

# Nutri Karakteri
st.markdown("""
<div class="nutri-box">
    🐱 <b>Nutri:</b> "Merhaba! Ben Nutri, senin AI diyetisyeninim! 💪 Bugün ne yemek istersin?"
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Kolonlar
col1, col2 = st.columns(2)

with col1:
    # 💧 Su Takibi
    st.markdown("### 💧 Su Tüketimi")
    
    # Progress bar (max 1.0 ile sınırla)
    water_progress = min(st.session_state.water_count / 8, 1.0)
    st.progress(water_progress, text=f"{st.session_state.water_count}/8 bardak")
    
    # Su butonu
    if st.button("💧 Su İçtim!", key="water_btn"):
        st.session_state.water_count += 1
        st.session_state.points += 10
        st.balloons()
        st.success(f"+10 puan! Toplam: {st.session_state.points} 💎")
        
        # Nutri mesajı
        if st.session_state.water_count < 4:
            st.markdown("🐱 **Nutri:** 'Harika gidiyorsun! 💪 Daha fazla su iç!'")
        elif st.session_state.water_count < 8:
            st.markdown("🐱 **Nutri:** 'Süper! Vücudun susuz kalmıyor. 🌊'")
        else:
            st.markdown("🐱 **Nutri:** 'WOOOW! Bugünlük hedefi tamamladın! 🎉'")
    
    # Su istatistikleri
    st.markdown(f"**Bugün:** {st.session_state.water_count} bardak | **Hedef:** 8 bardak")

with col2:
    # 🔥 Kalori Takibi
    st.markdown("### 🔥 Kalori Takibi")
    
    calorie_goal = 2000
    calorie_consumed = 1250  # Simüle
    
    st.metric("Harcanan", f"{calorie_consumed} kcal")
    st.metric("Hedef", f"{calorie_goal} kcal")
    
    progress_cal = min(calorie_consumed / calorie_goal, 1.0)
    st.progress(progress_cal, text=f"{int(progress_cal*100)}% tamamlandı")
    
    # Yemek ekle butonu
    if st.button("🍽️ Yemek Ekle"):
        st.info("Yemek ekleme formu yakında!")

st.markdown("---")

# Puan ve Streak
st.markdown("### 📊 İstatistikler")

col3, col4, col5 = st.columns(3)

with col3:
    st.metric("💎 Puan", st.session_state.points)
with col4:
    st.metric("🔥 Gün Serisi", f"{st.session_state.streak} gün")
with col5:
    st.metric("⚖️ Hedef Kilo", "75 kg")

st.markdown("---")

# AI Chat bölümü
st.markdown("### 💬 Nutri ile Konuş")

# Nutri avatar
st.markdown("""
<div style='text-align:center; margin:20px;'>
    <span style='font-size:60px;'>🐱</span>
    <p style='color:#ff9a56; font-size:20px;'><b>Nutri</b> - AI Diyetisyenin</p>
</div>
""", unsafe_allow_html=True)

# Sohbet
if prompt := st.text_input("Nutri'ye sor:", placeholder="Örnek: Bugün ne yemeliyim?"):
    st.markdown(f"**Sen:** {prompt}")
    
    # Nutri yanıtı (simüle)
    if "yemel" in prompt.lower() or "ne yem" in prompt.lower():
        st.markdown("""
        🐱 **Nutri:** "Bugün protein ağırlıklı beslenmelisin! 
        🍳 Kahvaltı: Yulaf + yumurta
        🥗 Öğle: Izgara tavuk + salata
        🐟 Akşam: Fırında somon
        💧 Arada suyunu içmeyi unutma!"
        """)
    elif "su" in prompt.lower():
        st.markdown("""
        🐱 **Nutri:** "Günlük 8 bardak su hedefine çalış! 💧 
        Şu an {}/8 bardakadasın. Devam!"
        """.format(st.session_state.water_count))
    else:
        st.markdown("""
        🐱 **Nutri:** "Harika soru! {0} hakkında sana yardımcı olabilirim. 
        Biraz daha detay verir misin? 😊"
        """.format(prompt[:20]))

# Sesli konuşma (yakında)
st.markdown("""
<div style='text-align:center; margin:30px;'>
    <p style='color:#666;'>🎤 <i>Sesli konuşma özelliği yakında...</i></p>
</div>
""")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;color:#666;'>© 2026 DiyetX - Nutri ile sağlıklı yaşam!</p>", unsafe_allow_html=True)