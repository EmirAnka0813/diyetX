"""
DiyetX - AI Destekli Diyet Uygulaması v3.0
Premium Landing Page + Kayıt Sistemi + Diyet Listesi
"""

import os

PORT = int(os.environ.get("PORT", 8080))

import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

st.set_page_config(page_title="DiyetX - Akıllı Diyet Asistanin", page_icon="🥗", layout="wide")

# === SENTRY ===
import sentry_sdk
sentry_sdk.init("https://97f83997b663a5a3545311ee0582c716@o4511259385397248.ingest.us.sentry.io/4511281486626816")

# === PREMIUM CSS ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0a0a; color: white; min-height: 100vh; }

.navbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 20px 50px; background: rgba(10,10,10,0.95);
    backdrop-filter: blur(20px); position: fixed; top: 0; left: 0; right: 0;
    z-index: 100; border-bottom: 1px solid rgba(255,255,255,0.1);
}
.logo { font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.nav-cta {
    background: linear-gradient(135deg, #667eea, #764ba2); color: white;
    padding: 10px 25px; border-radius: 50px; font-weight: 600; text-decoration: none;
}
.hero { min-height: 100vh; display: flex; flex-direction: column; justify-content: center;
    align-items: center; text-align: center; padding: 120px 20px 80px; }
.hero-badge {
    background: rgba(102,126,234,0.2); border: 1px solid rgba(102,126,234,0.3);
    padding: 8px 20px; border-radius: 50px; font-size: 14px; color: #667eea; margin-bottom: 30px;
}
.hero-title { font-size: clamp(48px, 8vw, 90px); font-weight: 800; line-height: 1.1; margin-bottom: 25px;
    background: linear-gradient(135deg, #fff 0%, #667eea 50%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -2px; }
.hero-subtitle { font-size: clamp(18px, 3vw, 24px); color: rgba(255,255,255,0.6);
    max-width: 600px; line-height: 1.6; margin-bottom: 40px; }
.hero-cta-group { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }
.btn-primary {
    background: linear-gradient(135deg, #667eea, #764ba2); color: white;
    padding: 18px 45px; border-radius: 50px; font-size: 18px; font-weight: 600;
    border: none; cursor: pointer; transition: all 0.3s; text-decoration: none;
}
.btn-primary:hover { transform: translateY(-3px); box-shadow: 0 20px 40px rgba(102,126,234,0.4); }
.btn-secondary {
    background: transparent; color: white; padding: 18px 45px; border-radius: 50px;
    font-size: 18px; font-weight: 600; border: 2px solid rgba(255,255,255,0.2);
    cursor: pointer; transition: all 0.3s; text-decoration: none;
}
.btn-secondary:hover { border-color: #667eea; background: rgba(102,126,234,0.1); }
.hero-stats { display: flex; gap: 60px; margin-top: 80px; }
.stat-number { font-size: 42px; font-weight: 800; background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.stat-label { font-size: 14px; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px; }
.nutri-float { font-size: 120px; margin-bottom: 20px; animation: bounce 2s infinite; }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
.features { padding: 120px 50px; background: linear-gradient(180deg, rgba(10,10,10,0) 0%, rgba(20,20,20,1) 100%); }
.section-tag { color: #667eea; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 15px; }
.section-title { font-size: clamp(36px, 5vw, 56px); font-weight: 800; margin-bottom: 20px; }
.section-desc { color: rgba(255,255,255,0.5); font-size: 18px; max-width: 600px; margin: 0 auto; }
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
.feature-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px; padding: 40px; transition: all 0.4s; }
.feature-card:hover { background: rgba(255,255,255,0.06); transform: translateY(-10px); border-color: rgba(102,126,234,0.3); }
.feature-icon { font-size: 50px; margin-bottom: 25px; }
.feature-title { font-size: 22px; font-weight: 700; margin-bottom: 15px; }
.feature-desc { color: rgba(255,255,255,0.5); line-height: 1.6; }
.diet-preview { padding: 120px 50px; background: #141414; }
.diet-card { background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
    border: 1px solid rgba(102,126,234,0.2); border-radius: 24px; padding: 50px; max-width: 900px; margin: 0 auto; }
.diet-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
.diet-day { font-size: 14px; color: #667eea; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; }
.diet-cal { background: rgba(102,126,234,0.2); padding: 5px 15px; border-radius: 20px; font-size: 14px; }
.meal-item { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.meal-info h4 { font-size: 18px; margin-bottom: 5px; }
.meal-info p { color: rgba(255,255,255,0.4); font-size: 14px; }
.meal-macros { text-align: right; color: rgba(255,255,255,0.5); font-size: 13px; }
.meal-macros span { margin-left: 15px; }
.cta-section { padding: 150px 50px; text-align: center; }
.cta-title { font-size: clamp(36px, 5vw, 60px); font-weight: 800; margin-bottom: 25px; }
.cta-subtitle { color: rgba(255,255,255,0.5); font-size: 20px; margin-bottom: 40px; }
.auth-section { display: flex; gap: 30px; justify-content: center; flex-wrap: wrap; padding: 0 20px; }
.auth-box { background: rgba(20,20,20,0.95); border: 1px solid rgba(255,255,255,0.1); border-radius: 30px;
    padding: 50px; width: 380px; backdrop-filter: blur(20px); }
.auth-title { font-size: 24px; font-weight: 700; text-align: center; margin-bottom: 30px; }
.input-field { width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px; padding: 15px 20px; color: white; font-size: 16px; outline: none; margin-bottom: 15px; }
.footer { background: #0a0a0a; border-top: 1px solid rgba(255,255,255,0.05); padding: 60px 50px 30px; }
.footer-brand { font-size: 24px; font-weight: 800; background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 15px; }
.footer-desc { color: rgba(255,255,255,0.4); line-height: 1.6; }
.footer-links { list-style: none; padding: 0; color: rgba(255,255,255,0.4); }
.footer-links a { color: rgba(255,255,255,0.4); text-decoration: none; }
.footer-links a:hover { color: #667eea; }
.footer-bottom { text-align: center; padding-top: 40px; margin-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.05); color: rgba(255,255,255,0.3); font-size: 14px; }
.nutri-box { background: linear-gradient(135deg, #ff9a56, #ff6b35); border-radius: 25px; padding: 25px; color: white; font-size: 18px; margin: 20px 0; }
::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #667eea; border-radius: 4px; }
@media (max-width: 768px) { .navbar { padding: 15px 20px; } .hero-stats { flex-direction: column; gap: 30px; } }
</style>
""", unsafe_allow_html=True)

# === SESSION STATES ===
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'step' not in st.session_state: st.session_state.step = 0
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

# === HELPER FUNCTIONS ===
def generate_diet_plan(name, current_weight, goal_weight, activity, diet_pref):
    plans = {
        "Serbest": {
            "Pazartesi": [("Yulaf + Meyve + Bal", 350, 12, 55, 10), ("Izgara Tavuk + Salata", 450, 38, 15, 22), ("Fırında Somon + Sebze", 420, 32, 18, 28), ("Bir Avuç Badem", 150, 5, 8, 12)],
            "Salı": [("Menemen + Ekmek", 300, 14, 25, 15), ("Kuru Fasulye + Pilav", 520, 22, 65, 18), ("Yoğurtlu Semizotu", 280, 12, 30, 12), ("Meyve", 90, 2, 22, 0)],
            "Çarşamba": [("Sütlaç + Ceviz", 380, 10, 58, 14), ("Adana Kebap + Lavaş", 580, 32, 42, 32), ("Mercimek Çorbası + Salata", 320, 14, 42, 8), ("Kuru İncir", 110, 2, 28, 0)],
            "Perşembe": [("Peynirli Omlet", 280, 18, 4, 22), ("Tavuk + Makarna + Salata", 520, 38, 55, 18), ("Sebzeli Güveç + Ekmek", 360, 10, 48, 14), ("Smoothie", 170, 6, 28, 4)],
            "Cuma": [("Simit + Peynir + Çay", 320, 12, 40, 14), ("Balık + Patates + Salata", 480, 34, 38, 24), ("Fasulye Pilaki", 380, 16, 52, 12), ("Havuç + Humus", 140, 4, 18, 6)],
            "Cumartesi": [("Serpme Kahvaltı", 480, 18, 38, 28), ("İskender + Ayran", 680, 32, 60, 30), ("Zeytinyağlı Enginar", 400, 8, 55, 16), ("Şeftali", 70, 1, 18, 0)],
            "Pazar": [("Kahvaltı Tabağı", 450, 20, 35, 26), ("Etli Nohut + Pilav", 550, 26, 62, 22), ("Baklava (2 dilim)", 380, 6, 48, 18), ("Fındık", 170, 4, 5, 16)]
        },
        "Düşük karbonhidrat": {
            "Pazartesi": [("Yumurta + Avokado", 320, 16, 8, 26), ("Salata + Tavuk", 280, 32, 6, 14), ("Et + Brokoli + Kaşar", 420, 38, 4, 26), ("Ceviz", 160, 4, 4, 16)],
            "Salı": [("Peynir + Domates", 180, 10, 4, 14), ("Ton Balığı Salatası", 260, 28, 2, 14), ("Tavuk Göğsü + Sebze", 320, 38, 6, 10), ("Badam", 140, 6, 6, 12)]
        },
        "Yüksek protein": {
            "Pazartesi": [("6 Yumurta Beyazı + Peynir", 420, 38, 4, 22), ("300g Tavuk + Pilav", 520, 48, 52, 14), ("250g Somon + Patates", 480, 42, 32, 20), ("Whey Smoothie", 240, 32, 18, 4)],
            "Salı": [("Yulaf + Protein Tozu", 380, 32, 48, 6), ("Kırmızı Et + Makarna", 580, 48, 52, 24), ("Baklava", 380, 6, 48, 18), ("Yoğurt + Fıstık", 190, 14, 18, 8)]
        },
        "Vejetaryen": {
            "Pazartesi": [("Yulaf + Meyve + Süt", 330, 10, 52, 8), ("Nohutlu Pilav + Salata", 420, 16, 68, 10), ("Izgara Sebze + Humus", 360, 14, 52, 12), ("Meyve", 90, 2, 22, 0)],
            "Salı": [("Smoothie Bowl + Granola", 300, 8, 52, 6), ("Mercimek Çorbası + Pilav", 380, 16, 62, 8), ("Sebze Güveç + Peynir", 330, 14, 32, 14), ("Badem", 140, 5, 8, 12)]
        }
    }
    return plans.get(diet_pref, plans["Serbest"])

# === LANDING PAGE (step=0) ===
if st.session_state.step == 0:
    st.markdown("""
    <nav class="navbar">
        <div class="logo">🥗 DiyetX</div>
        <a href="#features" style="color:rgba(255,255,255,0.7);text-decoration:none;margin-right:20px;">Özellikler</a>
        <a href="#diet" style="color:rgba(255,255,255,0.7);text-decoration:none;margin-right:20px;">Diyet</a>
        <a href="#auth" class="nav-cta">Ücretsiz Başla</a>
    </nav>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✨ Türkiye'nin En Akıllı Diyet Uygulaması</div>
        <div class="nutri-float">🐱</div>
        <h1 class="hero-title">Sağlığınızı<br>Yapay Zeka ile<br>Yönetin</h1>
        <p class="hero-subtitle">Kişisel diyet listeniz, AI destekli Nutri asistanınız ve motivasyon dolu gamifikasyon ile hedefinize ulaşın!</p>
        <div class="hero-cta-group">
            <a href="#auth" class="btn-primary">🎯 Hemen Başla</a>
            <a href="#features" class="btn-secondary">Özellikleri Gör</a>
        </div>
        <div class="hero-stats">
            <div><div class="stat-number">50K+</div><div class="stat-label">Aktif Kullanıcı</div></div>
            <div><div class="stat-number">4.9★</div><div class="stat-label">Uygulama Puanı</div></div>
            <div><div class="stat-number">1000+</div><div class="stat-label">Türk Yemeği</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <section class="features" id="features">
        <div style="text-align:center;margin-bottom:80px;">
            <div class="section-tag">Neden DiyetX?</div>
            <h2 class="section-title">Her Şey Sizin İçin Tasarlandı</h2>
            <p class="section-desc">En sevdiğiniz özellikler bir arada. Kolay, hızlı ve eğlenceli!</p>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🐱</div>
                <h3 class="feature-title">Nutri AI Asistan</h3>
                <p class="feature-desc">7/24 destek veren, motivasyon salan yapay zeka asistanın.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <h3 class="feature-title">Kişisel Diyet Listesi</h3>
                <p class="feature-desc">Hedeflerine göre oluşturulan haftalık diyet listesi. Türk mutfağına özel!</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📸</div>
                <h3 class="feature-title">Yemek Analizi</h3>
                <p class="feature-desc">Tabağının fotoğrafını çek, yapay zeka kalorini hesaplasın.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🏆</div>
                <h3 class="feature-title">Oyunlaştırma</h3>
                <p class="feature-desc">Puan topla, rozet kazan, streak tut. Kilo verme eğlenceli!</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💧</div>
                <h3 class="feature-title">Su Takibi</h3>
                <p class="feature-desc">Günlük su hedefini unutma. Hatırlatıcılarla!</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⏰</div>
                <h3 class="feature-title">Intermittent Fasting</h3>
                <p class="feature-desc">16:8, 18:6, 20:4... Senin için en uygun oruç programı!</p>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <section class="diet-preview" id="diet">
        <div style="text-align:center;margin-bottom:80px;">
            <div class="section-tag">Örnek Menü</div>
            <h2 class="section-title">Bugsün Ne Yiyebilirsin?</h2>
            <p class="section-desc">Sana özel hazırlanan lezzetli ve dengeli diyet listesi</p>
        </div>
        <div class="diet-card">
            <div class="diet-header">
                <span class="diet-day">📅 Pazartesi</span>
                <span class="diet-cal">🔥 1,370 kcal</span>
            </div>
            <div class="meal-item">
                <div class="meal-info"><h4>🍳 Kahvaltı</h4><p>Yulaf ezmesi + Meyve + Bal</p></div>
                <div class="meal-macros"><span>350 kcal</span><span>12g P</span><span>55g K</span></div>
            </div>
            <div class="meal-item">
                <div class="meal-info"><h4>🥗 Öğle</h4><p>Izgara tavuk + Salata</p></div>
                <div class="meal-macros"><span>450 kcal</span><span>38g P</span><span>15g K</span></div>
            </div>
            <div class="meal-item">
                <div class="meal-info"><h4>🍽️ Akşam</h4><p>Fırında somon + Sebze</p></div>
                <div class="meal-macros"><span>420 kcal</span><span>32g P</span><span>18g K</span></div>
            </div>
            <div class="meal-item" style="border:none;">
                <div class="meal-info"><h4>🥜 Atıştırmalık</h4><p>Bir avuç badem</p></div>
                <div class="meal-macros"><span>150 kcal</span><span>5g P</span><span>8g K</span></div>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <section class="cta-section" id="auth">
        <h2 class="cta-title">Hazır mısın?</h2>
        <p class="cta-subtitle">30 gün ücretsiz dene, farkı gör!</p>
    </section>
    """, unsafe_allow_html=True)
    
    with st.container():
        col_login, col_register = st.columns(2)
        with col_login:
            st.markdown('<div class="auth-box"><h3 class="auth-title">🔐 Giriş Yap</h3>', unsafe_allow_html=True)
            login_email = st.text_input("Email", placeholder="email@ornek.com", key="login_email", label_visibility="collapsed")
            login_password = st.text_input("Şifre", type="password", placeholder="Şifreni gir", key="login_pass", label_visibility="collapsed")
            if st.button("✅ Giriş Yap", use_container_width=True):
                if login_email and login_password:
                    if "@" in login_email and len(login_password) >= 6:
                        st.session_state.logged_in = True
                        st.session_state.user_name = login_email.split("@")[0].capitalize()
                        st.session_state.user_id = hashlib.md5(login_email.encode()).hexdigest()
                        st.session_state.step = 4
                        st.rerun()
                    else:
                        st.error("Email veya şifre hatalı!")
                else:
                    st.warning("Tüm alanları doldur!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_register:
            st.markdown('<div class="auth-box"><h3 class="auth-title">📝 Kayıt Ol</h3>', unsafe_allow_html=True)
            reg_name = st.text_input("Ad Soyad", placeholder="Adın ve soyadın", key="reg_name", label_visibility="collapsed")
            reg_email = st.text_input("Email", placeholder="email@ornek.com", key="reg_email", label_visibility="collapsed")
            reg_password = st.text_input("Şifre", type="password", placeholder="En az 6 karakter", key="reg_pass", label_visibility="collapsed")
            reg_password2 = st.text_input("Şifre Tekrar", type="password", placeholder="Tekrar gir", key="reg_pass2", label_visibility="collapsed")
            if st.button("✅ Kayıt Ol", use_container_width=True):
                if reg_name and reg_email and reg_password and reg_password2:
                    if "@" in reg_email:
                        if reg_password == reg_password2:
                            if len(reg_password) >= 6:
                                st.session_state.logged_in = True
                                st.session_state.user_name = reg_name
                                st.session_state.user_id = hashlib.md5(reg_email.encode()).hexdigest()
                                st.session_state.step = 3
                                st.rerun()
                            else:
                                st.error("Şifre en az 6 karakter!")
                        else:
                            st.error("Şifreler uyuşmuyor!")
                    else:
                        st.error("Geçerli bir email gir!")
                else:
                    st.warning("Tüm alanları doldur!")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <section class="footer">
        <div style="max-width:1200px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:50px;">
            <div>
                <div class="footer-brand">🥗 DiyetX</div>
                <p class="footer-desc">Türkiye'nin en akıllı diyet uygulaması. AI destekli Nutri ile hedefinize ulaşın!</p>
            </div>
            <div>
                <div style="font-weight:600;margin-bottom:20px;">Ürün</div>
                <ul class="footer-links"><li><a href="#features">Özellikler</a></li><li><a href="#diet">Diyet Listesi</a></li></ul>
            </div>
            <div>
                <div style="font-weight:600;margin-bottom:20px;">Şirket</div>
                <ul class="footer-links"><li><a href="#">Hakkımızda</a></li><li><a href="#">Blog</a></li></ul>
            </div>
            <div>
                <div style="font-weight:600;margin-bottom:20px;">Yasal</div>
                <ul class="footer-links"><li><a href="#">Gizlilik</a></li><li><a href="#">Şartlar</a></li><li><a href="#">KVKK</a></li></ul>
            </div>
        </div>
        <div class="footer-bottom">© 2026 DiyetX - Yapım: Emir Ünsal Aksu</div>
    </section>
    """, unsafe_allow_html=True)
    st.stop()

# === ONAOARDING (step=3) ===
elif st.session_state.step == 3:
    st.markdown("""
    <nav class="navbar"><div class="logo">🥗 DiyetX</div></nav>
    <div class="hero" style="min-height:auto;padding:150px 20px 50px;">
        <div class="hero-badge">🎯 Adım 2/3</div>
        <h1 class="hero-title" style="font-size:48px;">Hedeflerini Belirle</h1>
        <p class="hero-subtitle">Sana özel bir plan oluşturalım!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.current_weight = st.number_input("🏋️ Mevcut Kilo (kg)", 30, 200, 80, key="onboard_weight")
    with col2:
        st.session_state.goal_weight = st.number_input("🎯 Hedef Kilo (kg)", 30, 200, 75, key="onboard_goal")
    
    st.session_state.activity = st.selectbox("🏃 Aktivite Seviyesi", 
        ["Sedanter (az hareket)", "Hafif aktif (hafif spor)", "Orta (haftada 3-4 gün)", "Çok aktif (her gün spor)"])
    st.session_state.diet_pref = st.selectbox("🍽️ Diyet Tercihi", 
        ["Serbest", "Düşük karbonhidrat", "Yüksek protein", "Vejetaryen"])
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("📋 Diyet Listemi Oluştur!", use_container_width=True):
        st.session_state.diet_plan = generate_diet_plan(
            st.session_state.user_name, st.session_state.current_weight,
            st.session_state.goal_weight, st.session_state.activity, st.session_state.diet_pref
        )
        st.session_state.step = 4
        st.session_state.badges = ["🎯 İlk Adım", "📋 Diyet Listesi Oluşturuldu"]
        st.balloons()
        st.rerun()

# === ANA UYGULAMA (step=4) ===
elif st.session_state.step == 4:
    st.markdown("""
    <nav class="navbar">
        <div class="logo">🥗 DiyetX</div>
        <div style="color:white;">Hoş geldin, <b>""" + st.session_state.user_name + """</b>!</div>
    </nav>
    <br><br><br>
    """, unsafe_allow_html=True)
    
    col0, col1, col2 = st.columns(3)
    with col0:
        st.markdown('<div class="feature-card" style="text-align:center;"><span style="font-size:60px;">🔥</span><h1 style="font-size:60px;margin:0;">' + str(st.session_state.streak) + '</h1><p>Gün Serisi</p></div>', unsafe_allow_html=True)
    with col1:
        st.markdown('<div class="feature-card" style="text-align:center;"><span style="font-size:60px;">🏆</span><h1 style="font-size:60px;margin:0;">' + str(st.session_state.points) + '</h1><p>Puan</p></div>', unsafe_allow_html=True)
    with col2:
        badges_str = " ".join(st.session_state.badges[-3:]) if st.session_state.badges else "🎖️"
        st.markdown('<div class="feature-card" style="text-align:center;"><span style="font-size:60px;">🎖️</span><p style="font-size:20px;">' + badges_str + '</p><p>Rozetler</p></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="nutri-box">
        🐱 <b>Nutri:</b> "Merhaba """ + st.session_state.user_name + """! Bugün """ + str(st.session_state.calorie_today) + """ kcal yedin, """ + str(st.session_state.water_count) + """ bardak su içtin. Hedefine """ + str(max(0, st.session_state.current_weight - st.session_state.goal_weight)) + """ kg kaldı! 💪"
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Haftalık Diyet Listesi")
    
    if st.session_state.diet_plan:
        days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        selected_day = st.selectbox("Gün seç", days)
        
        if selected_day in st.session_state.diet_plan:
            day_meals = st.session_state.diet_plan[selected_day]
            total_cal = sum(m[1] for m in day_meals)
            meal_names = ["🍳 Kahvaltı", "🥗 Öğle", "🍽️ Akşam", "🥜 Atıştırmalık"]
            
            st.markdown("""
            <div class="diet-card" style="padding:30px;">
                <div class="diet-header">
                    <span class="diet-day">📅 {}</span>
                    <span class="diet-cal">🔥 {} kcal</span>
                </div>
            """.format(selected_day, total_cal), unsafe_allow_html=True)
            
            for i, meal_data in enumerate(day_meals):
                meal_food, meal_cal, meal_prot, meal_carb, meal_fat = meal_data
                color = "#27ae60" if meal_cal < 200 else "#f39c12" if meal_cal < 400 else "#e74c3c"
                emoji = "🟢" if meal_cal < 200 else "🟡" if meal_cal < 400 else "🔴"
                
                st.markdown("""
                <div class="meal-item">
                    <div class="meal-info"><h4>{} {}</h4><p>🍽️ {}</p></div>
                    <div class="meal-macros"><span style="color:{}">{} kcal</span><span>{}g P</span><span>{}g K</span><span>{}g Y</span></div>
                </div>
                """.format(emoji, meal_names[i], meal_food, color, meal_cal, meal_prot, meal_carb, meal_fat), unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 🍽️ Yemek Ekle")
    col_y1, col_y2 = st.columns([2, 1])
    yemek_adi = col_y1.text_input("Yemek", placeholder="Örnek: Tavuk salatası")
    yemek_kalori = col_y2.number_input("Kalori", 0, 2000, 200)
    col_m1, col_m2, col_m3 = st.columns(3)
    yemek_protein = col_m1.number_input("Protein (g)", 0, 200, 20)
    yemek_carbs = col_m2.number_input("Karbonhidrat (g)", 0, 300, 25)
    yemek_fat = col_m3.number_input("Yağ (g)", 0, 100, 10)
    emoji_map = "🟢" if yemek_kalori < 150 else "🟡" if yemek_kalori < 350 else "🔴"
    if st.button(f"➕ Ekle {emoji_map}"):
        st.session_state.calorie_today += yemek_kalori
        st.session_state.protein += yemek_protein
        st.session_state.carbs += yemek_carbs
        st.session_state.fat += yemek_fat
        st.session_state.points += 15
        st.success(f"{yemek_adi} eklendi! +{yemek_kalori} kcal")
        st.rerun()
    
    st.markdown("### 💧 Su Takibi")
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        water_pct = min(st.session_state.water_count / 8, 1.0)
        st.progress(water_pct, text=f"{st.session_state.water_count}/8 bardak")
        if st.button("💧 Su İçtim!", key="water"):
            st.session_state.water_count += 1
            st.session_state.points += 10
            st.balloons()
            st.rerun()
    with col_s2:
        st.info("💧 Su, metabolizmayı hızlandırır ve açlık hissini azaltır!")
    
    st.markdown("### 👟 Adım & Uyku")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.metric("Bugünkü Adım", f"{st.session_state.steps}", "adım")
        new_steps = st.number_input("Adım ekle", 0, 50000, 1000, key="steps")
        if st.button("👟 Ekle"):
            st.session_state.steps += new_steps
            st.session_state.points += 5
            st.rerun()
    with col_a2:
        st.metric("Uyku", f"{st.session_state.sleep_hours}h", "saat")
        new_sleep = st.slider("Uyku", 0, 12, 7, key="sleep")
        if st.button("😴 Kaydet"):
            st.session_state.sleep_hours = new_sleep
            if new_sleep >= 7 and "😴 İyi Uyku" not in st.session_state.badges:
                st.session_state.badges.append("😴 İyi Uyku")
                st.session_state.points += 20
            st.rerun()
    
    st.markdown("### ⏰ Intermittent Fasting")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fasting_plan = st.selectbox("Plan", ["Seç", "16:8", "18:6", "20:4", "5:2"])
        if not st.session_state.fasting_active:
            if st.button("▶️ Oruç Başlat"):
                st.session_state.fasting_active = True
                st.session_state.fasting_start = datetime.now()
                st.success("Oruç başladı! 🎉")
                st.rerun()
        else:
            elapsed = (datetime.now() - st.session_state.fasting_start).seconds
            hours, minutes = elapsed // 3600, (elapsed % 3600) // 60
            st.markdown(f"### ⏱️ {hours}s {minutes}dk")
            if st.button("⏹️ Bitir"):
                st.session_state.fasting_active = False
                st.session_state.points += 50
                if "⏰ Oruç Tamamlandı" not in st.session_state.badges:
                    st.session_state.badges.append("⏰ Oruç Tamamlandı")
                st.success("Oruç tamamlandı! +50 puan 🎉")
                st.rerun()
    with col_f2:
        st.markdown("#### Hatırlatıcılar")
        for r in st.session_state.meal_reminders:
            st.write(f"• {r}")
        new_r = st.text_input("Yeni hatırlatıcı", key="reminder")
        if st.button("🔔 Ekle") and new_r:
            st.session_state.meal_reminders.append(new_r)
            st.rerun()
    
    st.markdown("### 🧠 Duygusal Yeme Günlüğü")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        mood = st.selectbox("Ruh halin?", ["Mutlu", "Üzgün", "Stresli", "Sıkılmış", "Yorgun", "Endişeli"], key="mood")
        if st.button("📝 Kaydet"):
            st.session_state.emotional_log.append({"tarih": datetime.now().strftime("%d.%m.%Y %H:%M"), "ruh": mood, "kalori": st.session_state.calorie_today})
            st.session_state.points += 5
            st.success("Kaydedildi!")
    with col_e2:
        if st.session_state.emotional_log:
            for log in st.session_state.emotional_log[-5:]:
                emoji_m = "😊" if log["ruh"] == "Mutlu" else "😢" if log["ruh"] == "Üzgün" else "😰"
                st.write(f"{emoji_m} {log['tarih']} - {log['ruh']} ({log['kalori']} kcal)")
    
    st.markdown("### 💬 Nutri ile Konuş")
    if prompt := st.text_input("Nutri'ye sor...", placeholder="Örnek: Bugün ne yemeliyim?"):
        if any(x in prompt.lower() for x in ["yemel", "ne yem", "yemek"]):
            st.markdown("""
            <div class="nutri-box">
                🐱 <b>Nutri:</b> Harika! 🍳 Kahvaltı: Yulaf + meyve + yumurta (350 kcal)<br>
                Öğle: Izgara tavuk + salata (450 kcal)<br>
                Akşam: Fırında somon + sebze (400 kcal)<br>
                💧 Arada 2 bardak su!
            </div>
            """, unsafe_allow_html=True)
        elif "su" in prompt.lower():
            kalan = 8 - st.session_state.water_count
            st.markdown("""
            <div class="nutri-box">💧 Su çok önemli! Şu an {}/8 bardak. {} bardak daha iç! 💪</div>
            """.format(st.session_state.water_count, kalan), unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="nutri-box">🐱 <b>Nutri:</b> Harika soru! Sana yardımcı olmak için buradayım! 😊</div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:rgba(255,255,255,0.3);padding:30px;">
        © 2026 DiyetX - Nutri ile sağlıklı yaşam! 🐱<br>
        <small>Yapım: Emir Ünsal Aksu</small>
    </div>
    """, unsafe_allow_html=True)
