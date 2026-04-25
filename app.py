"""
DiyetX - AI Destekli Diyet Uygulaması
KYS Tarzı Modern Dashboard + Nutri Animasyonlu Karakter
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# === KURGU ===
st.set_page_config(
    page_title="DiyetX",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === CSS - Animasyonlar & Modern Tema ===
st.markdown("""
<style>
    /* Tema */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Kartlar */
    .metric-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Butonlar */
    .stButton > button {
        border-radius: 50px;
        padding: 15px 30px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    
    /* Sidebar */
    .sidebar .stRadio > label {
        font-size: 18px;
    }
    
    /* Nutri animasyonu */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    .nutri-float {
        animation: float 2s ease-in-out infinite;
    }
    
    /* Nutri kutusu */
    .nutri-box {
        background: linear-gradient(135deg, #ff9a56, #ff6b35);
        border-radius: 25px;
        padding: 25px;
        color: white;
        font-size: 18px;
        margin: 20px 0;
        border: 3px solid white;
        box-shadow: 0 10px 40px rgba(255,107,53,0.4);
    }
    
    /* Onboarding kartı */
    .onboard-card {
        background: white;
        border-radius: 30px;
        padding: 40px;
        max-width: 500px;
        margin: auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    }
    
    /* Progress steps */
    .step-active {
        background: linear-gradient(135deg, #00d4aa, #00b894);
        color: white;
        padding: 10px 20px;
        border-radius: 50px;
        display: inline-block;
    }
    .step-inactive {
        background: #e0e0e0;
        color: #999;
        padding: 10px 20px;
        border-radius: 50px;
        display: inline-block;
    }
    
    /* Tablo */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
    }
    .styled-table th {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 15px;
        text-align: left;
    }
    .styled-table td {
        padding: 12px 15px;
        border-bottom: 1px solid #eee;
    }
    .styled-table tr:hover {
        background: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if 'step' not in st.session_state:
    st.session_state.step = 0  # 0=onboarding, 1=anasayfa
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'goal_weight' not in st.session_state:
    st.session_state.goal_weight = 75
if 'current_weight' not in st.session_state:
    st.session_state.current_weight = 80
if 'water_count' not in st.session_state:
    st.session_state.water_count = 0
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'calorie_today' not in st.session_state:
    st.session_state.calorie_today = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0

# === ONAİBOARD EKRANI ===
if st.session_state.step == 0:
    # Ana ekran - sadece onboarding
    st.markdown("<h1 style='text-align:center;color:white;margin-top:50px;'>🥗 DiyetX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:white;font-size:20px;'>Sağlıklı beslen, hedefine ulaş!</p>", unsafe_allow_html=True)
    
    # Nutri animasyonlu
    st.markdown("""
    <div style='text-align:center;margin:40px 0;' class='nutri-float'>
        <span style='font-size:100px;'>🐱</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='onboard-card'>
        <h2 style='text-align:center;color:#667eea;'>Hoş Geldin!</h2>
        <p style='text-align:center;color:#666;'>Sana özel bir diyet deneyimi için önce tanışalım 😊</p>
        <br>
    """, unsafe_allow_html=True)
    
    # Form
    st.session_state.name = st.text_input("Adın nedir?", placeholder="Adını yaz...")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.current_weight = st.number_input("Mevcut kilon (kg)", min_value=30, max_value=200, value=80)
    with col2:
        st.session_state.goal_weight = st.number_input("Hedef kilon (kg)", min_value=30, max_value=200, value=75)
    
    activity = st.selectbox("Aktivite seviyen?", ["Sedanter (az hareket)", "Hafif aktif", "Orta derecede aktif", "Çok aktif"])
    
    diet_pref = st.selectbox("Diyet tercihin?", ["Kısıtlama yok", "Düşük karbonhidrat", "Yüksek protein", "Vejetaryen", "vegan"])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Hadi Başlayalım!"):
        if st.session_state.name:
            st.session_state.step = 1
            st.rerun()
        else:
            st.warning("Lütfen adını yaz!")
    
    st.stop()

# === ANA SAYFA ===
elif st.session_state.step == 1:
    # Header
    st.markdown("""
    <div style='background:white;border-radius:20px;padding:20px;margin-bottom:20px;'>
        <h2 style='margin:0;color:#667eea;'>🥗 DiyetX</h2>
        <p style='margin:0;color:#666;'>Hoş geldin, <b>{}</b>! 👋 Bugün nasılsın?</p>
    </div>
    """.format(st.session_state.name), unsafe_allow_html=True)
    
    # Nutri mesaj
    st.markdown("""
    <div class='nutri-box'>
        <span style='font-size:30px;' class='nutri-float'>🐱</span> 
        <b>Nutri:</b> "Merhaba {}! Bugün {} kcal yedin, {} bardak su içtin. 
        Hedefine {} kg kaldı! 💪 Devam et, başaracaksın!"
    </div>
    """.format(
        st.session_state.name,
        st.session_state.calorie_today,
        st.session_state.water_count,
        st.session_state.current_weight - st.session_state.goal_weight
    ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === METRİC KARTLAR ===
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color:#00d4aa;'>💧 Su</h3>
            <h1 style='font-size:50px;margin:0;'>{}/8</h1>
            <p style='color:#999;'>bardak</p>
        </div>
        """.format(st.session_state.water_count), unsafe_allow_html=True)
        
        if st.button("💧 Su İçtim!", key="water"):
            st.session_state.water_count += 1
            st.session_state.points += 10
            st.balloons()
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color:#ff6b35;'>🔥 Kalori</h3>
            <h1 style='font-size:50px;margin:0;'>{}</h1>
            <p style='color:#999;'>kcal / 2000</p>
        </div>
        """.format(st.session_state.calorie_today), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color:#667eea;'>⚖️ Kilo</h3>
            <h1 style='font-size:50px;margin:0;'>{}</h1>
            <p style='color:#999;'>kg / {}</p>
        </div>
        """.format(st.session_state.current_weight, st.session_state.goal_weight), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color:#f7c948;'>🏆 Puan</h3>
            <h1 style='font-size:50px;margin:0;'>{}</h1>
            <p style='color:#999;'>puan</p>
        </div>
        """.format(st.session_state.points), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === HIZLI İŞLEMLER ===
    st.markdown("### ⚡ Hızlı İşlemler")
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### 🍽️ Yemek Ekle")
        food_name = st.text_input("Yemek adı", placeholder="Örnek: Tavuk salatası")
        food_cal = st.number_input("Kalori", min_value=0, max_value=2000, value=200)
        
        if st.button("➕ Ekle", key="add_food"):
            if food_name:
                st.session_state.calorie_today += food_cal
                st.session_state.points += 15
                st.success(f"{food_name} eklendi! +{food_cal} kcal, +15 puan 🎉")
                st.rerun()
            else:
                st.warning("Yemek adı gerekli!")
    
    with col6:
        st.markdown("#### 📊 Bugün Ne Yedim?")
        
        # Son yemekler (simüle)
        if st.session_state.calorie_today > 0:
            yemekler = pd.DataFrame({
                "Yemek": ["Kahvaltı (Yulaf)", "Öğle (Tavuk)", "Atıştırmalık (Meyve)"],
                "Kalori": [350, 450, 100]
            })
            st.dataframe(yemekler, use_container_width=True)
        else:
            st.info("Henüz yemek eklemedin!")
    
    st.markdown("---")
    
    # === NUTRİ İLE SOHBET ===
    st.markdown("### 💬 Nutri ile Konuş")
    
    if prompt := st.text_input("Nutri'ye sor:", placeholder="Örnek: Bugün ne yemeliyim?"):
        
        if any(x in prompt.lower() for x in ["yemel", "ne yem", "yemek"]):
            st.markdown("""
            <div class='nutri-box'>
                <b>Nutri:</b> "{} için harika bir seçim! 
                🍳 Kahvaltı: Yulaf + meyve
                🥗 Öğle: Izgara tavuk + salata
                🐟 Akşam: Fırında somon
                💧 Arada 2 bardak su!"
            </div>
            """.format(st.session_state.name), unsafe_allow_html=True)
        elif any(x in prompt.lower() for x in ["su", "su iç"]):
            st.markdown("""
            <div class='nutri-box'>
                <b>Nutri:</b> "{} su çok önemli! 💧 
                Şu an {}/8 bardakadasın. 
                Hedefe ulaşman için {} bardak daha iç! 💪"
            </div>
            """.format(
                st.session_state.name,
                st.session_state.water_count,
                8 - st.session_state.water_count
            ), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='nutri-box'>
                <b>Nutri:</b> "Harika soru {}! 😊 
                Sana yardımcı olmak için buradayım. 
                Daha spesifik sorarsan daha iyi yardımcı olabilirim! 💬"
            </div>
            """.format(st.session_state.name), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === İLERLEME ===
    st.markdown("### 📈 İlerleme")
    
    # Progress bar'lar
    water_pct = min(st.session_state.water_count / 8 * 100, 100)
    calorie_pct = min(st.session_state.calorie_today / 2000 * 100, 100)
    weight_diff = max(0, (st.session_state.current_weight - st.session_state.goal_weight) / (st.session_state.current_weight - st.session_state.goal_weight + 10) * 100)
    
    st.markdown("""
    <table class='styled-table'>
        <tr><th>Özellik</th><th>Durum</th><th>Günlük Hedef</th></tr>
        <tr><td>💧 Su</td><td><div style='background:#e0e0e0;border-radius:10px;width:100%;height:20px;'><div style='background:linear-gradient(90deg,#00d4aa,#00b894);width:{}%;height:100%;border-radius:10px;'></div></div></td><td>{}/8 bardak</td></tr>
        <tr><td>🔥 Kalori</td><td><div style='background:#e0e0e0;border-radius:10px;width:100%;height:20px;'><div style='background:linear-gradient(90deg,#ff9a56,#ff6b35);width:{}%;height:100%;border-radius:10px;'></div></div></td><td>{}/2000 kcal</td></tr>
        <tr><td>⚖️ Kilo</td><td><div style='background:#e0e0e0;border-radius:10px;width:100%;height:20px;'><div style='background:linear-gradient(90deg,#667eea,#764ba2);width:{}%;height:100%;border-radius:10px;'></div></div></td><td>{} → {} kg</td></tr>
    </table>
    """.format(water_pct, st.session_state.water_count, calorie_pct, st.session_state.calorie_today, weight_diff, st.session_state.current_weight, st.session_state.goal_weight), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align:center;color:white;padding:20px;'>
        <p>© 2026 DiyetX - Nutri ile sağlıklı yaşam! 🐱</p>
        <p style='font-size:12px;'>Yapım: Emir Ünsal Aksu</p>
    </div>
    """, unsafe_allow_html=True)