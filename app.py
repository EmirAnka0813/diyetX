"""
DiyetX - AI Destekli Diyet Uygulaması v2.0
Kayıt Sistemi + Landing Page + Diyet Listesi
"""

import os

# Railway PORT ayarı
PORT = int(os.environ.get("PORT", 8080))

import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_module
import hashlib

st.set_page_config(page_title="DiyetX", page_icon="🥗", layout="wide")

# === FIREBASE CONFIG ===
# NOT: Gerçek Firebase config Railway environment variables'da olmalı
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY", "")
FIREBASE_AUTH_DOMAIN = os.environ.get("FIREBASE_AUTH_DOMAIN", "")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "")
FIREBASE_STORAGE_BUCKET = os.environ.get("FIREBASE_STORAGE_BUCKET", "")
FIREBASE_MESSAGING_SENDER_ID = os.environ.get("FIREBASE_MESSAGING_SENDER_ID", "")
FIREBASE_APP_ID = os.environ.get("FIREBASE_APP_ID", "")

# === CSS ===
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .metric-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .nutri-box {
        background: linear-gradient(135deg, #ff9a56, #ff6b35);
        border-radius: 25px;
        padding: 25px;
        color: white;
        font-size: 18px;
        margin: 20px 0;
    }
    .badge {
        background: linear-gradient(135deg, #f7c948, #f39c12);
        border-radius: 50px;
        padding: 10px 20px;
        color: white;
        display: inline-block;
        margin: 5px;
    }
    .streak-fire {
        font-size: 40px;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    .pulse { animation: pulse 2s infinite; }
    .food-green { color: #27ae60; font-weight: bold; }
    .food-yellow { color: #f39c12; font-weight: bold; }
    .food-red { color: #e74c3c; font-weight: bold; }
    .fasting-timer {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        color: white;
    }
    .landing-container {
        background: white;
        border-radius: 30px;
        padding: 40px;
        margin: 20px auto;
        max-width: 800px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    }
    .hero-title {
        font-size: 3em;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 20px;
    }
    .feature-card {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
    }
    .feature-icon {
        font-size: 3em;
        margin-bottom: 10px;
    }
    .cta-button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 50px;
        font-size: 1.2em;
        cursor: pointer;
        display: block;
        margin: 20px auto;
        width: 100%;
        max-width: 300px;
        text-align: center;
        text-decoration: none;
        transition: transform 0.3s;
    }
    .cta-button:hover {
        transform: scale(1.05);
    }
    .cta-secondary {
        background: white;
        color: #667eea;
        border: 2px solid #667eea;
    }
    .nutri-hero {
        font-size: 80px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    .diet-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
    .diet-meal {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
    }
    .login-box {
        background: white;
        border-radius: 20px;
        padding: 40px;
        max-width: 400px;
        margin: 50px auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    }
    div[data-testid="stForm"] {
        border: none;
        box-shadow: none;
    }
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #f8f9fa;
        border: none;
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# === SESSION STATES (kalıcı olması için) ===
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'step' not in st.session_state: st.session_state.step = 0  # 0=landing, 1=login, 2=register, 3=onboarding, 4=app
if 'goal_weight' not in st.session_state: st.session_state.goal_weight = 75
if 'current_weight' not in st.session_state: st.session_state.current_weight = 80
if 'water_count' not in st.session_state: st.session_state.water_count = 0
if 'points' not in st.session_state: st.session_state.points = 0
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'calorie_today' not in st.session_state: st.session_state.calorie_today = 0
if 'protein' not in st.session_state: st.session_state.protein = 0
if 'carbs' not in st.session_state: st.session_state.carbs = 0
if 'fat' not in st.session_state: st.session_state.fat = 0
if 'steps' not in st.session_state: st.session_state.steps = 0
if 'sleep_hours' not in st.session_state: st.session_state.sleep_hours = 0
if 'emotional_log' not in st.session_state: st.session_state.emotional_log = []
if 'badges' not in st.session_state: st.session_state.badges = []
if 'fasting_active' not in st.session_state: st.session_state.fasting_active = False
if 'fasting_start' not in st.session_state: st.session_state.fasting_start = None
if 'meal_reminders' not in st.session_state: st.session_state.meal_reminders = []
if 'diet_plan' not in st.session_state: st.session_state.diet_plan = None
if 'activity' not in st.session_state: st.session_state.activity = "Hafif aktif"
if 'diet_pref' not in st.session_state: st.session_state.diet_pref = "Serbest"

# === YARDIMCI FONKSİYONLAR ===
def hash_password(password):
    """Basit şifre hashleme (gerçek projede Firebase Auth kullanılmalı)"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_diet_plan(name, current_weight, goal_weight, activity, diet_pref):
    """Kişisel diyet listesi oluştur"""
    
    weight_to_lose = current_weight - goal_weight
    daily_calorie = 2000 - (weight_to_lose * 50)  # Basit hesap
    
    plans = {
        "Serbest": {
            "Pazartesi": {
                "Kahvaltı": ("Yulaf ezmesi + meyve + bal", 350, 15, 60, 10),
                "Öğle": ("Izgara tavuk + bulgur pilavı + salata", 500, 40, 50, 15),
                "Akşam": ("Fırında somon + sebze", 450, 35, 20, 25),
                "Atıştırmalık": ("Bir avuç badem", 150, 5, 8, 12)
            },
            "Salı": {
                "Kahvaltı": ("Menemen + tam buğday ekmeği", 300, 12, 30, 12),
                "Öğle": ("Kuru fasulye + pirinç + turşu", 550, 25, 70, 15),
                "Akşam": ("Yoğurtlu semizotu + ekmek", 350, 15, 40, 10),
                "Atıştırmalık": ("Meyve", 100, 2, 25, 0)
            },
            "Çarşamba": {
                "Kahvaltı": ("Sütlaç + ceviz", 400, 10, 65, 12),
                "Öğle": ("Adana kebap + lavaş + soğan", 600, 35, 45, 30),
                "Akşam": ("Mercimek çorbası + salata", 350, 15, 45, 10),
                "Atıştırmalık": ("Kuru incir", 120, 2, 30, 0)
            },
            "Perşembe": {
                "Kahvaltı": ("Peynirli omlet + domates", 280, 18, 5, 20),
                "Öğle": ("Tavuk ızgara + makarna + salata", 550, 40, 60, 18),
                "Akşam": ("Sebzeli güveç + ekmek", 380, 12, 50, 12),
                "Atıştırmalık": ("Smoothie (muz + süt)", 180, 8, 30, 3)
            },
            "Cuma": {
                "Kahvaltı": ("Açık ayran + peynir", 250, 12, 10, 15),
                "Öğle": ("Balık (levrek) + patates + salata", 500, 35, 40, 22),
                "Akşam": ("Fasulye pilaki + ekmek", 400, 18, 55, 12),
                "Atıştırmalık": ("Havuc + humus", 150, 5, 20, 6)
            },
            "Cumartesi": {
                "Kahvaltı": ("Simit + peynir + çay", 350, 12, 45, 14),
                "Öğle": ("İskender + ayran", 700, 35, 65, 28),
                "Akşam": ("Zeytinyağlı enginar + pilav", 420, 10, 60, 15),
                "Atıştırmalık": ("Şeftali", 80, 1, 20, 0)
            },
            "Pazar": {
                "Kahvaltı": ("Serpme kahvaltı (kaymak, bal, yumurta)", 500, 20, 40, 28),
                "Öğle": ("Etli nohut + pilav", 580, 28, 65, 20),
                "Akşam": ("Baklava (2 dilim)", 400, 8, 50, 20),
                "Atıştırmalık": ("Findık", 180, 4, 6, 16)
            }
        },
        "Düşük karbonhidrat": {
            "Pazartesi": {
                "Kahvaltı": ("Yumurta + avokado + zeytin", 350, 18, 10, 28),
                "Öğle": ("Salata + ızgara tavuk", 300, 35, 8, 15),
                "Akşam": ("Et + brokoli + kaşar", 450, 40, 5, 28),
                "Atıştırmalık": ("Ceviz", 180, 4, 4, 18)
            },
            "Salı": {
                "Kahvaltı": ("Peynir + domates + salatalık", 200, 12, 5, 15),
                "Öğle": ("Ton balığı salatası", 280, 30, 2, 15),
                "Akşam": ("Tavuk göğsü + sebze", 350, 40, 8, 12),
                "Atıştırmalık": ("Badam", 150, 6, 6, 12)
            }
        },
        "Yüksek protein": {
            "Pazartesi": {
                "Kahvaltı": ("6 yumurta beyazı + 2 tam yumurta + peynir", 450, 40, 5, 25),
                "Öğle": ("300g tavuk + pilav + salata", 550, 50, 55, 15),
                "Akşam": ("250g somon + patates", 500, 45, 35, 22),
                "Atıştırmalık": ("Whey protein smoothie", 250, 35, 20, 5)
            },
            "Salı": {
                "Kahvaltı": ("Yulaf + süt + muz + protein tozu", 400, 35, 50, 8),
                "Öğle": ("Kırmızı et + makarna + salata", 600, 50, 55, 25),
                "Akşam": ("Baklava (2 dilim)", 400, 8, 50, 20),
                "Atıştırmalık": ("Yoğurt + fıstık", 200, 15, 20, 8)
            }
        },
        "Vejetaryen": {
            "Pazartesi": {
                "Kahvaltı": ("Yulaf + meyve + süt", 350, 12, 55, 10),
                "Öğle": ("Nohutlu pilav + salata", 450, 18, 70, 12),
                "Akşam": ("Izgara sebze + humus + ekmek", 380, 15, 55, 12),
                "Atıştırmalık": ("Meyve", 100, 2, 25, 0)
            },
            "Salı": {
                "Kahvaltı": ("Smoothie bowl + granola", 320, 10, 55, 8),
                "Öğle": ("Mercimek çorbası + pilav", 400, 18, 65, 10),
                "Akşam": ("Sebze güveç + beyaz peynir", 350, 15, 35, 15),
                "Atıştırmalık": ("Badem", 150, 5, 8, 12)
            }
        }
    }
    
    return plans.get(diet_pref, plans["Serbest"])

# === LANDING PAGE (step=0) ===
if st.session_state.step == 0:
    st.markdown("<div class='landing-container'>", unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("<div class='nutri-hero'>🐱</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='hero-title'>DiyetX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-size:1.3em;color:#666;'>Akıllı Diyet Asistanın ile hedefine ulaş!</p>", unsafe_allow_html=True)
    
    # Nutri Tanıtım
    st.markdown("""
    <div style='background:linear-gradient(135deg,#ff9a56,#ff6b35);border-radius:20px;padding:30px;color:white;margin:30px 0;'>
        <h2 style='text-align:center;'>🐱 Nutri ile Tanış!</h2>
        <p style='text-align:center;font-size:1.1em;'>
            Seni tanıyan, motivasyon veren, <br>
            <b>yeşil yemekleri öneren</b> yapay zeka diyetisyenin!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Özellikler
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📸</div>
            <h4>Yemek Analizi</h4>
            <p>Tabağının fotoğrafını çek, kaloriyi öğren!</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📋</div>
            <h4>Kişisel Diyet</h4>
            <p>Hedefine özel haftalık diyet listesi!</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🏆</div>
            <h4>Oyunlaştırma</h4>
            <p>Puan topla, rozet kazan, streak tut!</p>
        </div>
        """, unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>💧</div>
            <h4>Su Takibi</h4>
            <p>Günlük su hedefini unutma!</p>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>⏰</div>
            <h4>IF Oruç</h4>
            <p>16:8, 18:6, 20:4 intermittent fasting</p>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🧠</div>
            <h4>Duygusal Yeme</h4>
            <p>Noom tarzı psikolojik destek!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Buttons
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Ücretsiz Başla", use_container_width=True):
        st.session_state.step = 2  # Register
        st.rerun()
    
    if st.button("🔐 Hesabım Var - Giriş Yap", use_container_width=True):
        st.session_state.step = 1  # Login
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# === LOGIN PAGE (step=1) ===
elif st.session_state.step == 1:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>🔐 Giriş Yap</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#666;'>Hesabına devam et</p>", unsafe_allow_html=True)
    
    login_email = st.text_input("📧 Email", placeholder="email@ornek.com")
    login_password = st.text_input("🔒 Şifre", type="password", placeholder="Şifreni gir")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✅ Giriş Yap", use_container_width=True):
            if login_email and login_password:
                # Basit doğrulama (gerçek projede Firebase Auth)
                if "@" in login_email and len(login_password) >= 6:
                    st.session_state.logged_in = True
                    st.session_state.user_name = login_email.split("@")[0].capitalize()
                    st.session_state.user_id = hashlib.md5(login_email.encode()).hexdigest()
                    st.session_state.step = 4  # Ana uygulama
                    st.success(f"Hoş geldin, {st.session_state.user_name}! 🎉")
                    st.rerun()
                else:
                    st.error("Email veya şifre hatalı!")
            else:
                st.warning("Lütfen tüm alanları doldur!")
    
    with col_btn2:
        if st.button("🔙 Geri", use_container_width=True):
            st.session_state.step = 0
            st.rerun()
    
    st.markdown("---", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888;font-size:0.9em;'>Hesabın yok mu? <a href='#' onclick='parent.document.getElementById(\"root\").children[0].children[1].children[0].children[0].children[1].children[0].children[0].children[0].children[0].children[0].click()'>Kayıt Ol</a></p>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# === REGISTER PAGE (step=2) ===
elif st.session_state.step == 2:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>📝 Kayıt Ol</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#666;'>Ücretsiz hesap oluştur</p>", unsafe_allow_html=True)
    
    reg_name = st.text_input("👤 Ad Soyad", placeholder="Adın ve soyadın")
    reg_email = st.text_input("📧 Email", placeholder="email@ornek.com")
    reg_password = st.text_input("🔒 Şifre", type="password", placeholder="En az 6 karakter")
    reg_password2 = st.text_input("🔒 Şifre Tekrar", type="password", placeholder="Tekrar gir")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("✅ Kayıt Ol", use_container_width=True):
            if reg_name and reg_email and reg_password and reg_password2:
                if "@" in reg_email:
                    if reg_password == reg_password2:
                        if len(reg_password) >= 6:
                            # Kayıt başarılı
                            st.session_state.logged_in = True
                            st.session_state.user_name = reg_name
                            st.session_state.user_id = hashlib.md5(reg_email.encode()).hexdigest()
                            st.session_state.step = 3  # Onboarding
                            st.success("Kayıt başarılı! 🎉 Şimdi hedeflerini belirle!")
                            st.rerun()
                        else:
                            st.error("Şifre en az 6 karakter olmalı!")
                    else:
                        st.error("Şifreler uyuşmuyor!")
                else:
                    st.error("Geçerli bir email gir!")
            else:
                st.warning("Lütfen tüm alanları doldur!")
    
    with col_btn2:
        if st.button("🔙 Geri", use_container_width=True):
            st.session_state.step = 0
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# === ONAOARDING (step=3) ===
elif st.session_state.step == 3:
    st.markdown("<div class='landing-container'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>🎯 Hedeflerini Belirle</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#666;'>Sana özel bir plan oluşturalım!</p>", unsafe_allow_html=True)
    
    col_o1, col_o2 = st.columns(2)
    with col_o1:
        st.session_state.current_weight = st.number_input("🏋️ Mevcut Kilo (kg)", 30, 200, 80, key="onboard_weight")
    with col_o2:
        st.session_state.goal_weight = st.number_input("🎯 Hedef Kilo (kg)", 30, 200, 75, key="onboard_goal")
    
    st.session_state.activity = st.selectbox("🏃 Aktivite Seviyesi", 
        ["Sedanter (az hareket)", "Hafif aktif (hafif spor)", "Orta (haftada 3-4 gün)", "Çok aktif (her gün spor)"])
    
    st.session_state.diet_pref = st.selectbox("🍽️ Diyet Tercihi", 
        ["Serbest", "Düşük karbonhidrat", "Yüksek protein", "Vejetaryen"])
    
    st.markdown("---", unsafe_allow_html=True)
    
    # Diyet planını oluştur
    if st.button("📋 Diyet Listemi Oluştur!", use_container_width=True):
        st.session_state.diet_plan = generate_diet_plan(
            st.session_state.user_name,
            st.session_state.current_weight,
            st.session_state.goal_weight,
            st.session_state.activity,
            st.session_state.diet_pref
        )
        st.session_state.step = 4
        st.session_state.badges = ["🎯 İlk Adım", "📋 Diyet Listesi Oluşturuldu"]
        st.balloons()
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# === ANA UYGULAMA (step=4) ===
elif st.session_state.step == 4:
    # Header
    st.markdown("""
    <div style='background:white;border-radius:20px;padding:20px;margin-bottom:20px;'>
        <h2 style='margin:0;color:#667eea;'>🥗 DiyetX</h2>
        <p style='margin:0;'>Hoş geldin, <b>{}</b>! 👋 <span style='float:right;font-size:0.8em;'><a href='#' onclick='window.location.reload()'>Çıkış</a></span></p>
    </div>
    """.format(st.session_state.user_name), unsafe_allow_html=True)
    
    # Streak & Puan
    col0, col1, col2 = st.columns(3)
    with col0:
        st.markdown("""
        <div class='metric-card'>
            <span class='streak-fire'>🔥</span>
            <h1 style='font-size:50px;margin:0;'>{}</h1>
            <p>Gün Serisi</p>
        </div>
        """.format(st.session_state.streak), unsafe_allow_html=True)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <span style='font-size:40px;'>🏆</span>
            <h1 style='font-size:50px;margin:0;'>{}</h1>
            <p>Puan</p>
        </div>
        """.format(st.session_state.points), unsafe_allow_html=True)
    with col2:
        badges_str = " ".join(st.session_state.badges[-3:]) if st.session_state.badges else "🎖️"
        st.markdown("""
        <div class='metric-card'>
            <span style='font-size:40px;'>🎖️</span>
            <p style='font-size:14px;'>{}</p>
            <p>Rozetler</p>
        </div>
        """.format(badges_str), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === NUTRİ MESAJ ===
    kalan_kalori = max(0, 2000 - st.session_state.calorie_today)
    kalan_kilo = max(0, st.session_state.current_weight - st.session_state.goal_weight)
    
    st.markdown("""
    <div class='nutri-box'>
        🐱 <b>Nutri:</b> "Merhaba {}! Bugün {} kcal yedin, {} bardak su içtin. 
        {} kcal kaldı! Hedefine {} kg kaldı! 💪"
    </div>
    """.format(
        st.session_state.user_name,
        st.session_state.calorie_today,
        st.session_state.water_count,
        kalan_kalori,
        kalan_kilo
    ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === DİYET LİSTESİ (YENİ!) ===
    st.markdown("### 📋 Haftalık Diyet Listesi")
    
    if st.session_state.diet_plan:
        days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        selected_day = st.selectbox("Gün seç", days)
        
        if selected_day in st.session_state.diet_plan:
            day_meals = st.session_state.diet_plan[selected_day]
            
            for meal_name, meal_data in day_meals.items():
                meal_food, meal_cal, meal_prot, meal_carb, meal_fat = meal_data
                
                if meal_cal < 200:
                    color = "#27ae60"
                    emoji = "🟢"
                elif meal_cal < 400:
                    color = "#f39c12"
                    emoji = "🟡"
                else:
                    color = "#e74c3c"
                    emoji = "🔴"
                
                st.markdown(f"""
                <div class='diet-card'>
                    <h4 style='margin:0 0 10px 0;color:#667eea;'>{} {}</h4>
                    <p style='margin:0;font-size:1.1em;'>🍽️ {}</p>
                    <div style='display:flex;justify-content:space-between;color:#666;font-size:0.9em;'>
                        <span>Kalori: <b style='color:{}'>{} kcal</b></span>
                        <span>Protein: {}g</span>
                        <span>Karb: {}g</span>
                        <span>Yağ: {}g</span>
                    </div>
                </div>
                """.format(emoji, meal_name, meal_food, color, meal_cal, meal_prot, meal_carb, meal_fat), unsafe_allow_html=True)
    else:
        st.warning("📋 Diyet listesi yok! Ayarlardan oluşturabilirsin.")
        if st.button("📋 Şimdi Oluştur!"):
            st.session_state.diet_plan = generate_diet_plan(
                st.session_state.user_name,
                st.session_state.current_weight,
                st.session_state.goal_weight,
                st.session_state.activity,
                st.session_state.diet_pref
            )
            st.rerun()
    
    st.markdown("---")
    
    # === KALORİ & MAKRO ===
    st.markdown("### 🔥 Kalori & Makro Takibi")
    
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.metric("Kalori", f"{st.session_state.calorie_today}", "kcal / 2000")
    with col_k2:
        st.metric("Protein", f"{st.session_state.protein}g", "g / 120")
    with col_k3:
        st.metric("Karbonhidrat", f"{st.session_state.carbs}g", "g / 200")
    with col_k4:
        st.metric("Yağ", f"{st.session_state.fat}g", "g / 65")
    
    # Makro bar
    protein_pct = min(st.session_state.protein / 120 * 100, 100)
    carbs_pct = min(st.session_state.carbs / 200 * 100, 100)
    fat_pct = min(st.session_state.fat / 65 * 100, 100)
    
    st.markdown(f"""
    <div style='background:white;border-radius:15px;padding:15px;margin:10px 0;'>
        <p style='margin:0;'><b>Protein</b> - {protein_pct:.0f}%</p>
        <div style='background:#e0e0e0;border-radius:10px;height:15px;'><div style='background:#e74c3c;width:{protein_pct}%;height:100%;border-radius:10px;'></div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:white;border-radius:15px;padding:15px;margin:10px 0;'>
        <p style='margin:0;'><b>Karbonhidrat</b> - {carbs_pct:.0f}%</p>
        <div style='background:#e0e0e0;border-radius:10px;height:15px;'><div style='background:#f39c12;width:{carbs_pct}%;height:100%;border-radius:10px;'></div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background:white;border-radius:15px;padding:15px;margin:10px 0;'>
        <p style='margin:0;'><b>Yağ</b> - {fat_pct:.0f}%</p>
        <div style='background:#e0e0e0;border-radius:10px;height:15px;'><div style='background:#27ae60;width:{fat_pct}%;height:100%;border-radius:10px;'></div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # === YEMEK GİRİŞİ ===
    st.markdown("#### 🍽️ Yemek Ekle")
    
    col_y1, col_y2, col_y3 = st.columns(3)
    with col_y1:
        yemek_adi = st.text_input("Yemek", placeholder="Örnek: Tavuk salatası", key="yemek_input")
    with col_y2:
        yemek_kalori = st.number_input("Kalori", 0, 2000, 200, key="yemek_kalori")
    with col_y3:
        yemek_tip = st.selectbox("Tür", ["Kahvaltı", "Öğle", "Akşam", "Atıştırmalık"], key="yemek_tip")
    
    # Makro girişi
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        yemek_protein = st.number_input("Protein (g)", 0, 200, 20, key="yemek_prot")
    with col_m2:
        yemek_carbs = st.number_input("Karbonhidrat (g)", 0, 300, 25, key="yemek_carb")
    with col_m3:
        yemek_fat = st.number_input("Yağ (g)", 0, 100, 10, key="yemek_fat")
    
    # Renk puanı (Noom tarzı)
    if yemek_kalori < 150:
        renk_class = "food-green"
        renk_emoji = "🟢"
    elif yemek_kalori < 350:
        renk_class = "food-yellow"
        renk_emoji = "🟡"
    else:
        renk_class = "food-red"
        renk_emoji = "🔴"
    
    if st.button(f"➕ Ekle {renk_emoji}", key="yemek_ekle"):
        st.session_state.calorie_today += yemek_kalori
        st.session_state.protein += yemek_protein
        st.session_state.carbs += yemek_carbs
        st.session_state.fat += yemek_fat
        st.session_state.points += 15
        
        if st.session_state.calorie_today >= 2000 and len(st.session_state.badges) < 5:
            st.session_state.badges.append("🔥 Günlük Hedef")
        
        st.success(f"{yemek_adi} eklendi! +{yemek_kalori} kcal")
        st.rerun()
    
    st.markdown("---")
    
    # === SU TAKİBİ ===
    st.markdown("### 💧 Su Takibi")
    
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        water_pct = min(st.session_state.water_count / 8, 1.0)
        st.progress(water_pct, text=f"{st.session_state.water_count}/8 bardak")
        
        if st.button("💧 Su İçtim!", key="water_btn"):
            st.session_state.water_count += 1
            st.session_state.points += 10
            st.balloons()
            st.rerun()
    
    with col_s2:
        st.markdown("#### 💧 Neden Su İçmeliyiz?")
        st.info("Su, metabolizmayı hızlandırır, toksinleri atar ve açlık hissini azaltır! 💪")
    
    st.markdown("---")
    
    # === ADIM & AKTİVİTE ===
    st.markdown("### 👟 Adım & Aktivite")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.metric("Bugünkü Adım", f"{st.session_state.steps}", "adım / 10,000")
        new_steps = st.number_input("Adım ekle", 0, 50000, 1000, key="steps_input")
        if st.button("👟 Adım Ekle", key="steps_btn"):
            st.session_state.steps += new_steps
            st.session_state.points += 5
            st.rerun()
    
    with col_a2:
        st.metric("Uyku", f"{st.session_state.sleep_hours}h", "saat / 8")
        new_sleep = st.slider("Uyku saati", 0, 12, 7, key="sleep_slider")
        if st.button("😴 Uyku Kaydet", key="sleep_btn"):
            st.session_state.sleep_hours = new_sleep
            if new_sleep >= 7:
                if "😴 İyi Uyku" not in st.session_state.badges:
                    st.session_state.badges.append("😴 İyi Uyku")
                st.session_state.points += 20
            st.rerun()
    
    st.markdown("---")
    
    # === INTERMITTENT FASTING ===
    st.markdown("### ⏰ Intermittent Fasting")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fasting_plan = st.selectbox("Fasting Planı", ["Seç", "16:8", "18:6", "20:4", "5:2"], key="fasting_plan")
        
        if not st.session_state.fasting_active:
            if st.button("▶️ Oruç Başlat", key="fasting_start"):
                st.session_state.fasting_active = True
                st.session_state.fasting_start = datetime.now()
                st.success("Oruç başladı! 🎉")
                st.rerun()
        else:
            elapsed = (datetime.now() - st.session_state.fasting_start).seconds
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            
            st.markdown(f"""
            <div class='fasting-timer'>
                <h2>⏱️ {hours}s {minutes}dk</h2>
                <p>Oruç devam ediyor...</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("⏹️ Orucu Bitir", key="fasting_stop"):
                st.session_state.fasting_active = False
                st.session_state.points += 50
                if "⏰ Oruç Tamamlandı" not in st.session_state.badges:
                    st.session_state.badges.append("⏰ Oruç Tamamlandı")
                st.success("Oruç tamamlandı! +50 puan 🎉")
                st.rerun()
    
    with col_f2:
        st.markdown("#### 🕐 Öğün Hatırlatıcıları")
        for i, reminder in enumerate(st.session_state.meal_reminders):
            st.write(f"• {reminder}")
        
        new_reminder = st.text_input("Hatırlatıcı ekle", placeholder="Örnek: 08:00 - Kahvaltı", key="reminder_input")
        if st.button("🔔 Ekle", key="reminder_btn") and new_reminder:
            st.session_state.meal_reminders.append(new_reminder)
            st.rerun()
    
    st.markdown("---")
    
    # === DUYGUSAL YEME GÜNLÜĞÜ ===
    st.markdown("### 🧠 Duygusal Yeme Günlüğü (Noom Tarzı)")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        mood = st.selectbox("Şu anki ruh halin?", ["Mutlu", "Üzgün", "Stresli", "Sıkılmış", "Yorgun", "Endişeli"], key="mood_select")
        if st.button("📝 Kaydet", key="mood_btn"):
            st.session_state.emotional_log.append({
                "tarih": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "ruh": mood,
                "kalori": st.session_state.calorie_today
            })
            st.session_state.points += 5
            st.success("Kaydedildi!")
    
    with col_e2:
        if st.session_state.emotional_log:
            st.markdown("#### 📊 Son Kayıtlar")
            for log in st.session_state.emotional_log[-5:]:
                emoji = "😊" if log["ruh"] == "Mutlu" else "😢" if log["ruh"] == "Üzgün" else "😰"
                st.write(f"{emoji} {log['tarih']} - {log['ruh']} ({log['kalori']} kcal)")
    
    st.markdown("---")
    
    # === NUTRİ İLE SOHBET ===
    st.markdown("### 💬 Nutri ile Konuş")
    
    if prompt := st.text_input("Nutri'ye sor:", placeholder="Örnek: Bugün ne yemeliyim?", key="nutri_input"):
        
        if any(x in prompt.lower() for x in ["yemel", "ne yem", "yemek", "list", "diyet"]):
            st.markdown("""
            <div class='nutri-box'>
                <b>🐱 Nutri:</b> "{} için harika! 🍳
                Kahvaltı: Yulaf + meyve + yumurta (350 kcal)
                Öğle: Izgara tavuk + salata (450 kcal)
                Akşam: Fırında somon + sebze (400 kcal)
                💧 Arada 2 bardak su iç!"
            </div>
            """.format(st.session_state.user_name), unsafe_allow_html=True)
        elif "su" in prompt.lower():
            kalan = 8 - st.session_state.water_count
            st.markdown("""
            <div class='nutri-box'>
                <b>🐱 Nutri:</b> "{} su çok önemli! 💧 
                Şu an {}/8 bardak. {} bardak daha iç! 💪"
            </div>
            """.format(st.session_state.user_name, st.session_state.water_count, kalan), unsafe_allow_html=True)
        elif "oruç" in prompt.lower() or "fasting" in prompt.lower():
            st.markdown("""
            <div class='nutri-box'>
                <b>🐱 Nutri:</b> "Intermittent fasting harika! ⏰
                16:8 = 16 saat oruç, 8 saat yemek
                18:6 = 18 saat oruç, 6 saat yemek
                Hangisini tercih edersin? 😊"
            </div>
            """, unsafe_allow_html=True)
        elif "kilo" in prompt.lower() or "hedef" in prompt.lower():
            st.markdown(f"""
            <div class='nutri-box'>
                <b>🐱 Nutri:</b> "{} hedefine ulaşacağız! 🎯
                Mevcut kilo: {st.session_state.current_weight} kg
                Hedef kilo: {st.session_state.goal_weight} kg
                Kalan: {st.session_state.current_weight - st.session_state.goal_weight} kg
                Bunu başaracağız! 💪"
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='nutri-box'>
                <b>🐱 Nutri:</b> "Harika soru {}! 😊 
                Sana yardımcı olmak için buradayım! Biraz daha açık anlatırsan daha iyi yardımcı olabilirim!"
            </div>
            """.format(st.session_state.user_name), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === LİDERLİK TABLOSU ===
    st.markdown("### 🏆 Liderlik Tablosu (Yakında)")
    
    st.info("👥 Arkadaşını davet et, birlikte yarışın! (Yakında)")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align:center;color:white;padding:20px;'>
        <p>© 2026 DiyetX - Nutri ile sağlıklı yaşam! 🐱</p>
        <p style='font-size:12px;'>Yapım: Emir Ünsal Aksu</p>
    </div>
    """, unsafe_allow_html=True)
