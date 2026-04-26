"""
DiyetX - AI Destekli Diyet Uygulamasi v3.2
Premium Landing Page - Turuncu/Mor/Siyah Tema + Animasyonlu Yemek Arka Plani
"""

import os

PORT = int(os.environ.get("PORT", 8080))

import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

st.set_page_config(page_title="DiyetX - Akilli Diyet Asistanin", page_icon="", layout="wide")

# === SENTRY ===
import sentry_sdk
sentry_sdk.init("https://97f83997b663a5a3545311ee0582c716@o4511259385397248.ingest.us.sentry.io/4511281486626816")

# === PREMIUM CSS ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #000000; color: white; min-height: 100vh; overflow-x: hidden; }

/* Animated Food Background */
.food-bg {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 0; overflow: hidden; pointer-events: none;
}
.food-fall {
    position: absolute; font-size: 25px; opacity: 0.03; animation: foodFall linear infinite;
}
@keyframes foodFall {
    0% { transform: translateY(-50px) rotate(0deg); opacity: 0; }
    10% { opacity: 0.06; }
    90% { opacity: 0.06; }
    100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
}

.navbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 20px 50px; background: rgba(0,0,0,0.9);
    backdrop-filter: blur(20px); position: fixed; top: 0; left: 0; right: 0;
    z-index: 100; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.logo { font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #ff9a56, #e040fb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.nav-cta {
    background: linear-gradient(135deg, #ff9a56, #e040fb); color: white;
    padding: 10px 25px; border-radius: 50px; font-weight: 600; text-decoration: none;
    box-shadow: 0 4px 15px rgba(255,154,86,0.4);
}
.hero { min-height: 100vh; display: flex; flex-direction: column; justify-content: center;
    align-items: center; text-align: center; padding: 120px 20px 80px; position: relative; z-index: 1; }
.hero-badge {
    background: linear-gradient(135deg, rgba(255,154,86,0.2), rgba(224,64,251,0.2));
    border: 1px solid rgba(255,154,86,0.3); padding: 8px 20px; border-radius: 50px; font-size: 14px; color: #ff9a56; margin-bottom: 30px;
}
.hero-title { font-size: clamp(48px, 8vw, 90px); font-weight: 800; line-height: 1.1; margin-bottom: 25px;
    background: linear-gradient(135deg, #ffffff 0%, #ff9a56 50%, #e040fb 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -2px; }
.hero-subtitle { font-size: clamp(18px, 3vw, 24px); color: rgba(255,255,255,0.7);
    max-width: 600px; line-height: 1.6; margin-bottom: 40px; }
.hero-cta-group { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }
.btn-primary {
    background: linear-gradient(135deg, #ff9a56, #e040fb); color: white;
    padding: 18px 45px; border-radius: 50px; font-size: 18px; font-weight: 600;
    border: none; cursor: pointer; transition: all 0.3s; text-decoration: none;
    box-shadow: 0 10px 30px rgba(255,154,86,0.4);
}
.btn-primary:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 20px 40px rgba(224,64,251,0.4); }
.btn-secondary {
    background: transparent; color: white; padding: 18px 45px; border-radius: 50px;
    font-size: 18px; font-weight: 600; border: 2px solid rgba(224,64,251,0.5);
    cursor: pointer; transition: all 0.3s; text-decoration: none;
}
.btn-secondary:hover { border-color: #e040fb; background: rgba(224,64,251,0.1); }
.hero-stats { display: flex; gap: 60px; margin-top: 80px; }
.stat-number { font-size: 42px; font-weight: 800; background: linear-gradient(135deg, #ff9a56, #e040fb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.stat-label { font-size: 14px; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 1px; }
.nutri-float { font-size: 120px; margin-bottom: 20px; animation: bounce 2s infinite; }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
.features { padding: 120px 50px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(20,0,20,0.8) 50%, rgba(0,0,0,0) 100%); position: relative; z-index: 1; }
.section-tag { color: #e040fb; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 15px; }
.section-title { font-size: clamp(36px, 5vw, 56px); font-weight: 800; margin-bottom: 20px; background: linear-gradient(135deg, #fff, #ff9a56); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.section-desc { color: rgba(255,255,255,0.5); font-size: 18px; max-width: 600px; margin: 0 auto; }
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
.feature-card { background: linear-gradient(135deg, rgba(255,154,86,0.08), rgba(224,64,251,0.08));
    border: 1px solid rgba(255,154,86,0.15); border-radius: 24px; padding: 40px; transition: all 0.4s; }
.feature-card:hover { background: linear-gradient(135deg, rgba(255,154,86,0.15), rgba(224,64,251,0.15)); transform: translateY(-10px); box-shadow: 0 20px 40px rgba(224,64,251,0.2); border-color: rgba(224,64,251,0.4); }
.feature-icon { font-size: 50px; margin-bottom: 25px; }
.feature-title { font-size: 22px; font-weight: 700; margin-bottom: 15px; color: #fff; }
.feature-desc { color: rgba(255,255,255,0.6); line-height: 1.6; }
.diet-preview { padding: 120px 50px; background: rgba(20,0,20,0.5); position: relative; z-index: 1; }
.diet-card { background: linear-gradient(135deg, rgba(255,154,86,0.1), rgba(224,64,251,0.1));
    border: 1px solid rgba(255,154,86,0.2); border-radius: 24px; padding: 50px; max-width: 900px; margin: 0 auto; }
.diet-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
.diet-day { font-size: 14px; color: #ff9a56; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; }
.diet-cal { background: linear-gradient(135deg, #ff9a56, #e040fb); padding: 5px 15px; border-radius: 20px; font-size: 14px; color: white; }
.meal-item { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.meal-info h4 { font-size: 18px; margin-bottom: 5px; color: #fff; }
.meal-info p { color: rgba(255,255,255,0.5); font-size: 14px; }
.meal-macros { text-align: right; color: #e040fb; font-size: 13px; }
.meal-macros span { margin-left: 15px; }
.cta-section { padding: 150px 50px; text-align: center; background: linear-gradient(180deg, rgba(20,0,20,0.5) 0%, rgba(0,0,0,1) 100%); position: relative; z-index: 1; }
.cta-title { font-size: clamp(36px, 5vw, 60px); font-weight: 800; margin-bottom: 25px; background: linear-gradient(135deg, #ff9a56, #e040fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.cta-subtitle { color: rgba(255,255,255,0.6); font-size: 20px; margin-bottom: 40px; }
.auth-section { display: flex; gap: 30px; justify-content: center; flex-wrap: wrap; padding: 0 20px; position: relative; z-index: 1; }
.auth-box { background: linear-gradient(135deg, rgba(255,154,86,0.08), rgba(224,64,251,0.08)); border: 1px solid rgba(224,64,251,0.2); border-radius: 30px;
    padding: 50px; width: 380px; backdrop-filter: blur(20px); }
.auth-title { font-size: 24px; font-weight: 700; text-align: center; margin-bottom: 30px; background: linear-gradient(135deg, #ff9a56, #e040fb); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.input-field { width: 100%; background: rgba(255,255,255,0.03); border: 1px solid rgba(224,64,251,0.2);
    border-radius: 12px; padding: 15px 20px; color: white; font-size: 16px; outline: none; margin-bottom: 15px; transition: border-color 0.3s; }
.input-field:focus { border-color: #ff9a56; }
.input-field::placeholder { color: rgba(255,255,255,0.3); }
.footer { background: #000000; border-top: 1px solid rgba(224,64,251,0.1); padding: 60px 50px 30px; position: relative; z-index: 1; }
.footer-brand { font-size: 24px; font-weight: 800; background: linear-gradient(135deg, #ff9a56, #e040fb);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 15px; }
.footer-desc { color: rgba(255,255,255,0.4); line-height: 1.6; }
.footer-links { list-style: none; padding: 0; color: rgba(255,255,255,0.4); }
.footer-links a { color: rgba(255,255,255,0.4); text-decoration: none; transition: color 0.3s; }
.footer-links a:hover { color: #ff9a56; }
.footer-bottom { text-align: center; padding-top: 40px; margin-top: 40px;
    border-top: 1px solid rgba(255,255,255,0.05); color: rgba(255,255,255,0.3); font-size: 14px; }
.nutri-box { background: linear-gradient(135deg, #ff9a56, #e040fb); border-radius: 25px; padding: 25px; color: white; font-size: 18px; margin: 20px 0; box-shadow: 0 10px 30px rgba(255,154,86,0.3); }
::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #ff9a56, #e040fb); border-radius: 4px; }
@media (max-width: 768px) { .navbar { padding: 15px 20px; } .hero-stats { flex-direction: column; gap: 30px; } }
</style>
""", unsafe_allow_html=True)

# === ANIMATED FOOD BACKGROUND ===
# Using food emoji with better styling
food_icons = ["🍎","🥗","🥑","🥕","🍇","🥦","🍳","🥩","🐟","🍅","🫐","🥐","🍠","🍊","🥭","🍋","🥜","🥛"]

food_images = [
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=100",  # salad
    "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=100",  # apple
    "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=100",  # avocado
    "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=100",  # carrot
    "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=100",  # grapes
    "https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?w=100",  # broccoli
    "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=100",  # egg
    "https://images.unsplash.com/photo-1544025162-d76694265947?w=100",  # meat
    "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=100",  # fish
    "https://images.unsplash.com/photo-1546470427-0d4db154cce8?w=100",  # tomato
]

import random

st.markdown('<div class="food-bg">', unsafe_allow_html=True)
# Create more randomized food positions
food_items = []
for i in range(80):
    food_items.append({
        'img': food_images[i % len(food_images)] if i < len(food_images) else food_icons[i % len(food_icons)],
        'left': random.randint(0, 95),
        'delay': round(random.uniform(0, 20), 1),
        'duration': random.randint(12, 25)
    })

for item in food_items:
    img_html = f'<img src="{item["img"]}" style="width:40px;height:40px;object-fit:cover;border-radius:8px;opacity:0.8;" loading="lazy">'
    st.markdown(f'<div class="food-fall" style="left:{item["left"]}%;animation-delay:{item["delay"]}s;animation-duration:{item["duration"]}s;">{img_html}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

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
            "Pazartesi": [("Yulaf + Meyve + Bal", 350, 12, 55, 10), ("Izgara Tavuk + Salata", 450, 38, 15, 22), ("Firinda Somon + Sebze", 420, 32, 18, 28), ("Bir Avuc Badem", 150, 5, 8, 12)],
            "Sali": [("Menemen + Ekmek", 300, 14, 25, 15), ("Kuru Fasulye + Pilav", 520, 22, 65, 18), ("Yogurtlu Semizotu", 280, 12, 30, 12), ("Meyve", 90, 2, 22, 0)],
            "Carsamba": [("Sutlac + Ceviz", 380, 10, 58, 14), ("Adana Kebap + Lavas", 580, 32, 42, 32), ("Mercimek Corbasi + Salata", 320, 14, 42, 8), ("Kuru Incir", 110, 2, 28, 0)],
            "Persembe": [("Peynirli Omlet", 280, 18, 4, 22), ("Tavuk + Makarna + Salata", 520, 38, 55, 18), ("Sebzeli Guvec + Ekmek", 360, 10, 48, 14), ("Smoothie", 170, 6, 28, 4)],
            "Cuma": [("Simit + Peynir + Cay", 320, 12, 40, 14), ("Balik + Patates + Salata", 480, 34, 38, 24), ("Fasulye Pilaki", 380, 16, 52, 12), ("Havuc + Humus", 140, 4, 18, 6)],
            "Cumartesi": [("Serpme Kahvalti", 480, 18, 38, 28), ("Iskender + Ayran", 680, 32, 60, 30), ("Zeytinyagli Enginar", 400, 8, 55, 16), ("Seftali", 70, 1, 18, 0)],
            "Pazar": [("Kahvalti Tabagi", 450, 20, 35, 26), ("Etli Nohut + Pilav", 550, 26, 62, 22), ("Baklava (2 dilim)", 380, 6, 48, 18), ("Findik", 170, 4, 5, 16)]
        },
        "Dusuk karbonhidrat": {
            "Pazartesi": [("Yumurta + Avokado", 320, 16, 8, 26), ("Salata + Tavuk", 280, 32, 6, 14), ("Et + Brokoli + Kesar", 420, 38, 4, 26), ("Ceviz", 160, 4, 4, 16)],
            "Sali": [("Peynir + Domates", 180, 10, 4, 14), ("Ton Baligi Salatasi", 260, 28, 2, 14), ("Tavuk Gogsu + Sebze", 320, 38, 6, 10), ("Badam", 140, 6, 6, 12)],
            "Carsamba": [("Yumurta + Peynir", 280, 20, 4, 20), ("Salata + Ton Baligi", 250, 28, 5, 12), ("Tavuk Gögüsü + Sebze", 300, 35, 8, 14), ("Zeytin", 120, 2, 6, 10)],
            "Persembe": [("Avokado + Yumurta", 300, 14, 10, 24), ("Yoğurtlu Tavuk", 270, 30, 8, 12), ("Balik + Salata", 320, 32, 6, 16), ("Ceviz", 160, 4, 4, 16)],
            "Cuma": [("Peynirli Omlet", 260, 18, 4, 18), ("Ton Baligi Salatasi", 240, 26, 4, 12), ("Et + Brokoli", 350, 35, 6, 20), ("Badam", 140, 6, 6, 12)],
            "Cumartesi": [("Yumurta Beyazi + Sebze", 200, 16, 4, 12), ("Salata + Tavuk", 280, 32, 6, 14), ("Balik + Tatlı Patates", 340, 30, 28, 14), ("Peynir", 150, 8, 2, 12)],
            "Pazar": [("Avokado Toast + Yumurta", 320, 14, 22, 22), ("Yoğurt + Kuruyemis", 260, 14, 24, 12), ("Tavuk + Quinoa", 360, 34, 28, 12), ("Smoothie", 180, 6, 22, 6)]
        },
        "Yuksek protein": {
            "Pazartesi": [("6 Yumurta Beyazi + Peynir", 420, 38, 4, 22), ("300g Tavuk + Pilav", 520, 48, 52, 14), ("250g Somon + Patates", 480, 42, 32, 20), ("Whey Smoothie", 240, 32, 18, 4)],
            "Sali": [("Yulaf + Protein Tozu", 380, 32, 48, 6), ("Kirmizi Et + Makarna", 580, 48, 52, 24), ("Baklava", 380, 6, 48, 18), ("Yogurt + Fistik", 190, 14, 18, 8)],
            "Carsamba": [("5 Yumurta + Peynir", 380, 32, 4, 24), ("Ton Baligi + Pilav", 500, 45, 48, 18), ("Tavuk Gögüsü + Makarna", 520, 46, 54, 16), ("Protein Bar", 220, 20, 22, 8)],
            "Persembe": [("Smoothie + Protein", 360, 30, 44, 10), ("350g Kirmizi Et + Sebze", 550, 50, 20, 30), ("Yumurta + Ekmek", 380, 24, 30, 18), ("Yoğurt + Ceviz", 280, 18, 16, 18)],
            "Cuma": [("4 Yumurta + Peynir", 340, 28, 4, 22), ("Balik + Patates", 480, 42, 38, 22), ("Tavuk + quino", 500, 48, 40, 16), ("Kuru Uzum + Findik", 200, 4, 24, 10)],
            "Cumartesi": [("Pankek + Protein", 420, 32, 50, 12), ("300g Et + Pilav", 600, 52, 56, 22), ("Somon + Tatlı Patates", 520, 44, 36, 24), ("Protein Shake", 200, 25, 10, 4)],
            "Pazar": [("Kahvalti: 3 Yumurta + Sucuk", 480, 30, 8, 34), ("Kirmizi Et + Bulgur", 580, 48, 44, 26), ("Pilav + Nohut", 520, 22, 68, 16), ("Findik + Badem", 240, 6, 12, 20)]
        },
        "Vejetaryen": {
            "Pazartesi": [("Yulaf + Meyve + Sut", 330, 10, 52, 8), ("Nohutlu Pilav + Salata", 420, 16, 68, 10), ("Izgara Sebze + Humus", 360, 14, 52, 12), ("Meyve", 90, 2, 22, 0)],
            "Sali": [("Smoothie Bowl + Granola", 300, 8, 52, 6), ("Mercimek Corbasi + Pilav", 380, 16, 62, 8), ("Sebze Guvec + Peynir", 330, 14, 32, 14), ("Badam", 140, 5, 8, 12)],
            "Carsamba": [("Avokado Toast + Yumurta", 320, 14, 22, 22), ("Leblebi + Domates", 260, 10, 36, 8), ("Falafel + Pilav", 420, 16, 58, 14), ("Meyve", 100, 2, 24, 0)],
            "Persembe": [("Sütlaç + Ceviz", 340, 10, 54, 12), ("Kuru Fasulye + Pilav", 400, 18, 62, 10), ("Sebze Corbasi + Ekmek", 280, 12, 42, 8), ("Peynir", 150, 8, 2, 12)],
            "Cuma": [("Menemen + Ekmek", 300, 14, 25, 15), ("Nohutlu Yaprak Sarma", 350, 14, 40, 14), ("Izgara Peynir + Salata", 320, 16, 12, 20), ("Zeytin", 120, 2, 6, 10)],
            "Cumartesi": [("Simit + Peynir + Cay", 320, 12, 40, 14), ("Mantarli Pilav + Salata", 380, 14, 52, 12), ("Sebze Güveç + Yoğurt", 340, 16, 36, 14), ("Meyve", 90, 2, 22, 0)],
            "Pazar": [("Serpme Kahvalti", 400, 16, 38, 22), ("Mercimek Corbasi + Pilav", 400, 18, 64, 10), ("Izgara Sebze + Humus", 360, 14, 48, 12), ("Kuru Incir", 110, 2, 28, 0)]
        }
    }
    return plans.get(diet_pref, plans["Serbest"])

# === LANDING PAGE (step=0) ===
if st.session_state.step == 0:
    st.markdown('<nav class="navbar"><div class="logo">DiyetX</div><a href="#features" style="color:rgba(255,255,255,0.7);text-decoration:none;margin-right:20px;">Ozellikler</a><a href="#diet" style="color:rgba(255,255,255,0.7);text-decoration:none;margin-right:20px;">Diyet</a><a href="#auth" class="nav-cta">Ucretsiz Basla</a></nav>', unsafe_allow_html=True)
    
    st.markdown('<div class="hero"><div class="hero-badge">Turkiye\'nin En Akilli Diyet Uygulamasi</div><div class="nutri-float">🐱</div><h1 class="hero-title">Sagliginizi<br>Yapay Zeka ile<br>Yonetxin</h1><p class="hero-subtitle">Kisisel diyet listeniz, AI destekli Nutri asistaniniz ve motivasyon dolu gamifikasyon ile hedefinize ulasin!</p><div class="hero-cta-group"><a href="#auth" class="btn-primary">Hemen Basla - Ucretsiz</a><a href="#features" class="btn-secondary">Ozellikleri Gor</a></div><div class="hero-stats"><div><div class="stat-number">50K+</div><div class="stat-label">Aktif Kullanici</div></div><div><div class="stat-number">4.9</div><div class="stat-label">Uygulama Puani</div></div><div><div class="stat-number">1000+</div><div class="stat-label">Turk Yemegi</div></div></div></div>', unsafe_allow_html=True)
    
    st.markdown('<section class="features" id="features"><div style="text-align:center;margin-bottom:80px;"><div class="section-tag">Neden DiyetX?</div><h2 class="section-title">Her Sey Sizin Icin Tasarlandi</h2><p class="section-desc">En sevdiyiniz ozellikler bir arada. Kolay, hizli ve eglenceli!</p></div><div class="features-grid"><div class="feature-card"><div class="feature-icon">ASISTAN</div><h3 class="feature-title">Nutri AI Asistan</h3><p class="feature-desc">7/24 destek veren, motivasyon salan yapay zeka asistanin.</p></div><div class="feature-card"><div class="feature-icon">LISTE</div><h3 class="feature-title">Kisisel Diyet Listesi</h3><p class="feature-desc">Hedeflerine gore olusturulan haftalik diyet listesi. Turk mutfagina ozel!</p></div><div class="feature-card"><div class="feature-icon">KAMERA</div><h3 class="feature-title">Yemek Analizi</h3><p class="feature-desc">Tabaginin fotografini cek, yapay zeka kalorini hesaplasin.</p></div><div class="feature-card"><div class="feature-icon">ROZET</div><h3 class="feature-title">Oyunlastirma</h3><p class="feature-desc">Puan topla, rozet kazan, streak tut. Kilo verme eglenceli!</p></div><div class="feature-card"><div class="feature-icon">SU</div><h3 class="feature-title">Su Takibi</h3><p class="feature-desc">Gunluk su hedefini unutma. Hatirlatgilarla!</p></div><div class="feature-card"><div class="feature-icon">SAAT</div><h3 class="feature-title">Intermittent Fasting</h3><p class="feature-desc">16:8, 18:6, 20:4... Senin icin en uygun oruc programi!</p></div></div></section>', unsafe_allow_html=True)
    
    st.markdown('<section class="diet-preview" id="diet"><div style="text-align:center;margin-bottom:80px;"><div class="section-tag">Ornek Menu</div><h2 class="section-title">Bugun Ne Yiyebilirsin?</h2><p class="section-desc">Sana ozel hazirlanan lezzetli ve dengeli diyet listesi</p></div><div class="diet-card"><div class="diet-header"><span class="diet-day">Pazartesi</span><span class="diet-cal">1370 kcal</span></div><div class="meal-item"><div class="meal-info"><h4>Kahvalti (08:00)</h4><p>Yulaf ezmesi + Meyve + Bal</p></div><div class="meal-macros"><span>350 kcal</span><span>12g P</span><span>55g K</span></div></div><div class="meal-item"><div class="meal-info"><h4>Ogle (12:30)</h4><p>Izgara tavuk + Salata</p></div><div class="meal-macros"><span>450 kcal</span><span>38g P</span><span>15g K</span></div></div><div class="meal-item"><div class="meal-info"><h4>Aksam (19:00)</h4><p>Firin da somon + Sebze</p></div><div class="meal-macros"><span>420 kcal</span><span>32g P</span><span>18g K</span></div></div><div class="meal-item" style="border:none;"><div class="meal-info"><h4>Atistirma (15:00)</h4><p>Bir avuc badem</p></div><div class="meal-macros"><span>150 kcal</span><span>5g P</span><span>8g K</span></div></div></div></section>', unsafe_allow_html=True)
    
    st.markdown('<section class="cta-section" id="auth"><h2 class="cta-title">Hazir misin?</h2><p class="cta-subtitle">30 gun ucretsiz dene, farki gor!</p></section>', unsafe_allow_html=True)
    
    col_login, col_register = st.columns(2)
    with col_login:
        st.markdown('<div class="auth-box"><h3 class="auth-title">Giris Yap</h3>', unsafe_allow_html=True)
        login_email = st.text_input("Email", placeholder="email@ornek.com", key="login_email", label_visibility="collapsed")
        login_password = st.text_input("Sifre", type="password", placeholder="Sifreni gir", key="login_pass", label_visibility="collapsed")
        if st.button("Giris Yap", use_container_width=True):
            if login_email and login_password:
                if "@" in login_email and len(login_password) >= 6:
                    st.session_state.logged_in = True
                    st.session_state.user_name = login_email.split("@")[0].capitalize()
                    st.session_state.user_id = hashlib.md5(login_email.encode()).hexdigest()
                    st.session_state.step = 4
                    st.rerun()
                else:
                    st.error("Email veya sifre hatasi!")
            else:
                st.warning("Tum alanlari doldur!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_register:
        st.markdown('<div class="auth-box"><h3 class="auth-title">Kayit Ol</h3>', unsafe_allow_html=True)
        reg_name = st.text_input("Ad Soyad", placeholder="Adin ve soyadin", key="reg_name", label_visibility="collapsed")
        reg_email = st.text_input("Email", placeholder="email@ornek.com", key="reg_email", label_visibility="collapsed")
        reg_password = st.text_input("Sifre", type="password", placeholder="En az 6 karakter", key="reg_pass", label_visibility="collapsed")
        reg_password2 = st.text_input("Sifre Tekrar", type="password", placeholder="Tekrar gir", key="reg_pass2", label_visibility="collapsed")
        if st.button("Kayit Ol", use_container_width=True):
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
                            st.error("Sifre en az 6 karakter!")
                    else:
                        st.error("Sifreler uyusmuyor!")
                else:
                    st.error("Gecerli bir email gir!")
            else:
                st.warning("Tum alanlari doldur!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<section class="footer"><div style="max-width:1200px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:50px;"><div><div class="footer-brand">DiyetX</div><p class="footer-desc">Turkiye\'nin en akillidir. AI destekli Nutri ile hedefinize ulasin!</p></div><div><div style="font-weight:600;margin-bottom:20px;">Urun</div><ul class="footer-links"><li><a href="#features">Ozellikler</a></li><li><a href="#diet">Diyet Listesi</a></li></ul></div><div><div style="font-weight:600;margin-bottom:20px;">Sirket</div><ul class="footer-links"><li><a href="#">Hakkimizda</a></li><li><a href="#">Blog</a></li></ul></div><div><div style="font-weight:600;margin-bottom:20px;">Yasal</div><ul class="footer-links"><li><a href="#">Gizlilik</a></li><li><a href="#">Sartlar</a></li><li><a href="#">KVKK</a></li></ul></div></div><div class="footer-bottom">(c) 2026 DiyetX - Yapim: Emir Unsal Aksu</div></section>', unsafe_allow_html=True)
    st.stop()

# === ONAOARDING (step=3) ===
elif st.session_state.step == 3:
    st.markdown('<nav class="navbar"><div class="logo">DiyetX</div></nav><div class="hero" style="min-height:auto;padding:150px 20px 50px;"><div class="hero-badge">Adim 2/3</div><h1 class="hero-title" style="font-size:48px;">Hedeflerini Belirle</h1><p class="hero-subtitle">Sana ozel bir plan olusturalim!</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.current_weight = st.number_input("Mevcut Kilo (kg)", 30, 200, 80, key="onboard_weight")
    with col2:
        st.session_state.goal_weight = st.number_input("Hedef Kilo (kg)", 30, 200, 75, key="onboard_goal")
    
    st.session_state.activity = st.selectbox("Aktivite Seviyesi", 
        ["Sedanter (az hareket)", "Hafif aktif (hafif spor)", "Orta (haftada 3-4 gun)", "Cok aktif (her gun spor)"])
    st.session_state.diet_pref = st.selectbox("Diyet Tercihi", 
        ["Serbest", "Dusuk karbonhidrat", "Yuksek protein", "Vejetaryen"])
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("Diyet Listemi Olustur!", use_container_width=True):
        st.session_state.diet_plan = generate_diet_plan(
            st.session_state.user_name, st.session_state.current_weight,
            st.session_state.goal_weight, st.session_state.activity, st.session_state.diet_pref
        )
        st.session_state.step = 4
        st.session_state.badges = ["Ilk Adim", "Diyet Listesi Olusturuldu"]
        st.balloons()
        st.rerun()

# === ANA UYGULAMA (step=4) ===
elif st.session_state.step == 4:
    st.markdown('<nav class="navbar"><div class="logo">DiyetX</div><div style="color:white;">Hos geldin, <b>' + st.session_state.user_name + '</b>!</div></nav><br><br><br>', unsafe_allow_html=True)
    
    col0, col1, col2 = st.columns(3)
    with col0:
        st.markdown('<div class="feature-card" style="text-align:center;"><span style="font-size:60px;">AKTAR</span><h1 style="font-size:60px;margin:0;">' + str(st.session_state.streak) + '</h1><p>Gun Serisi</p></div>', unsafe_allow_html=True)
    with col1:
        st.markdown('<div class="feature-card" style="text-align:center;"><span style="font-size:60px;">PUAN</span><h1 style="font-size:60px;margin:0;">' + str(st.session_state.points) + '</h1><p>Puan</p></div>', unsafe_allow_html=True)
    with col2:
        badges_str = " ".join(st.session_state.badges[-3:]) if st.session_state.badges else "Rozet"
        st.markdown('<div class="feature-card" style="text-align:center;"><span style="font-size:60px;">ROZET</span><p style="font-size:20px;">' + badges_str + '</p><p>Rozetler</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="nutri-box">Nutri: Merhaba ' + st.session_state.user_name + '! Bugun ' + str(st.session_state.calorie_today) + ' kcal yedin, ' + str(st.session_state.water_count) + ' bardak su icdin. Hedefine ' + str(max(0, st.session_state.current_weight - st.session_state.goal_weight)) + ' kg kaldi!</div>', unsafe_allow_html=True)
    
    st.markdown("### Haftalik Diyet Listesi")
    
    if st.session_state.diet_plan:
        days = ["Pazartesi", "Sali", "Carsamba", "Persembe", "Cuma", "Cumartesi", "Pazar"]
        today = days[datetime.now().weekday()]
        
        # Bugunkü gunü vurgula
        col_nav1, col_nav2 = st.columns([1, 3])
        with col_nav1:
            if st.button("BUGUN", use_container_width=True):
                selected_day = today
            else:
                selected_day = st.selectbox("Gun secin", days, index=days.index(today) if today in days else 0)
        with col_nav2:
            st.markdown("<small style='color:#e040fb;'>Haftanin gunlerini gor ve kendi diet planina gore yemeklerini sec!</small>", unsafe_allow_html=True)
        
        if selected_day in st.session_state.diet_plan:
            day_meals = st.session_state.diet_plan[selected_day]
            total_cal = sum(m[1] for m in day_meals)
            meal_names = ["Kahvalti (08:00)", "Ogle (12:30)", "Aksam (19:00)", "Atistirma (15:00)"]
            
            diet_html = '<div class="diet-card" style="padding:30px;"><div class="diet-header"><span class="diet-day">' + selected_day + '</span><span class="diet-cal">' + str(total_cal) + ' kcal</span></div>'
            st.markdown(diet_html, unsafe_allow_html=True)
            
            for i, meal_data in enumerate(day_meals):
                meal_food, meal_cal, meal_prot, meal_carb, meal_fat = meal_data
                color = "#27ae60" if meal_cal < 200 else "#f39c12" if meal_cal < 400 else "#e74c3c"
                
                st.markdown('<div class="meal-item"><div class="meal-info"><h4>' + meal_names[i] + '</h4><p>' + meal_food + '</p></div><div class="meal-macros"><span style="color:' + color + '">' + str(meal_cal) + ' kcal</span><span>' + str(meal_prot) + 'g P</span><span>' + str(meal_carb) + 'g K</span><span>' + str(meal_fat) + 'g Y</span></div></div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### Yemek Ekle")
    col_y1, col_y2 = st.columns([2, 1])
    yemek_adi = col_y1.text_input("Yemek", placeholder="Ornek: Tavuk salatasi")
    yemek_kalori = col_y2.number_input("Kalori", 0, 2000, 200)
    col_m1, col_m2, col_m3 = st.columns(3)
    yemek_protein = col_m1.number_input("Protein (g)", 0, 200, 20)
    yemek_carbs = col_m2.number_input("Karbonhidrat (g)", 0, 300, 25)
    yemek_fat = col_m3.number_input("Yag (g)", 0, 100, 10)
    emoji_map = "YESIL" if yemek_kalori < 150 else "SARI" if yemek_kalori < 350 else "KIRMIZI"
    if st.button(f"Ekle {emoji_map}"):
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
        st.progress(water_pct, text=f"💧 {st.session_state.water_count}/8 bardak")
        if st.button("Su Ictim!", key="water"):
            st.session_state.water_count += 1
            st.session_state.points += 10
            st.balloons()
            st.rerun()
    with col_s2:
        st.markdown('<div style="background:linear-gradient(135deg,rgba(0,180,216,0.2),rgba(0,150,200,0.2));border-radius:15px;padding:20px;text-align:center;"><span style="font-size:50px;">💧</span><h3 style="color:white;margin:10px 0;">Neden Su Ic Meliyiz?</h3><p style="color:rgba(255,255,255,0.7);margin:0;">Metabolizmayi hizlandirir, toksinleri atar, aclik hissini azaltir!</p></div>', unsafe_allow_html=True)
    
    st.markdown("### Adim ve Uyku")
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.metric("Bugunku Adim", f"{st.session_state.steps}", "adim")
        new_steps = st.number_input("Adim ekle", 0, 50000, 1000, key="steps")
        if st.button("Ekle"):
            st.session_state.steps += new_steps
            st.session_state.points += 5
            st.rerun()
    with col_a2:
        st.metric("Uyku", f"{st.session_state.sleep_hours}h", "saat")
        new_sleep = st.slider("Uyku", 0, 12, 7, key="sleep")
        if st.button("Kaydet"):
            st.session_state.sleep_hours = new_sleep
            if new_sleep >= 7 and "IyI Uyku" not in st.session_state.badges:
                st.session_state.badges.append("IyI Uyku")
                st.session_state.points += 20
            st.rerun()
    
    st.markdown("### Intermittent Fasting")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fasting_plan = st.selectbox("Plan", ["Sec", "16:8", "18:6", "20:4", "5:2"])
        if not st.session_state.fasting_active:
            if st.button("Oruc Baslat"):
                st.session_state.fasting_active = True
                st.session_state.fasting_start = datetime.now()
                st.success("Oruc basladi!")
                st.rerun()
        else:
            elapsed = (datetime.now() - st.session_state.fasting_start).seconds
            hours, minutes = elapsed // 3600, (elapsed % 3600) // 60
            st.markdown(f"### {hours}s {minutes}dk")
            if st.button("Bitir"):
                st.session_state.fasting_active = False
                st.session_state.points += 50
                if "Oruc Tamamlandi" not in st.session_state.badges:
                    st.session_state.badges.append("Oruc Tamamlandi")
                st.success("Oruc tamamlandi! +50 puan")
                st.rerun()
    with col_f2:
        st.markdown("#### Hatirlatmalar")
        for r in st.session_state.meal_reminders:
            st.write(f"- {r}")
        new_r = st.text_input("Yeni hatirlatma", key="reminder")
        if st.button("Ekle") and new_r:
            st.session_state.meal_reminders.append(new_r)
            st.rerun()
    
    st.markdown("### Duygusal Yeme Gunlugu")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        mood = st.selectbox("Ruh halin?", ["Mutlu", "Uzgun", "Stresli", "Sikilmis", "Yorgun", "Endiseseli"], key="mood")
        if st.button("Kaydet"):
            st.session_state.emotional_log.append({"tarih": datetime.now().strftime("%d.%m.%Y %H:%M"), "ruh": mood, "kalori": st.session_state.calorie_today})
            st.session_state.points += 5
            st.success("Kaydedildi!")
    with col_e2:
        if st.session_state.emotional_log:
            for log in st.session_state.emotional_log[-5:]:
                emoji_m = ":)" if log["ruh"] == "Mutlu" else ":(" if log["ruh"] == "Uzgun" else ":o"
                st.write(f"{emoji_m} {log['tarih']} - {log['ruh']} ({log['kalori']} kcal)")
    
    st.markdown("### Nutri ile Konus")
    if prompt := st.text_input("Nutri'ye sor...", placeholder="Ornek: Pilav yerine ne yiyebilirim?"):
        prompt_lower = prompt.lower()
        
        # Yemek degisikligi onerlri - DENGELI CEVAP
        if any(x in prompt_lower for x in ["degistir", "farkli", "baska", "yerine", " alternatif"]):
            st.markdown('<div class="nutri-box">Nutri: Tabii! Diyet listenize uygun alternatifler:<br><br><b>Pilav yerine:</b><br>- Bulgur pilavi (ayni kaloride, daha fazla lif)<br>- Tam bugday ekmek (biraz daha az kalorili)<br>- Patates püresi (nadir kullanilir, dikkat)<br><br><b>Tavuk yerine:</b><br>- Balik (daha az kalorili, omega-3!)<br>- Yumurta (aynı protein, daha ucuz)<br>- Tofu (vejetaryen secenegi)<br><br><b>Meyve yerine:</b><br>- Kuruyemis (daha kalorili, porsiyon kontrolu!)<br>- Yogurt (protein deposu!)<br>- Peynir (kalorili ama kalsiyum!</div>', unsafe_allow_html=True)
        
        # Soru-cevap formatinda - DENGELI
        elif any(x in prompt_lower for x in ["yiyebilir", "yiyebilir miyim", "yebilir miyim", "mide"]):
            st.markdown('<div class="nutri-box">Nutri: Bu besinler hakkinda bilgi:<br><br> YESIL Olur: Salata, meyve, tavuk gögusun, yumurta, sebze<br><br> SARI Dikkat: Pilav, makarna, ekmek (porsiyon kontrolu lazim!)<br><br> KIRMIZI Kacin: Kizarik et, islenmis gidalar, sekerli icecekler<br><br>Her besin diyet planina uygun miktarda tukenebilir!</div>', unsafe_allow_html=True)
        
        elif any(x in prompt_lower for x in ["ne yemel", "yemel", "menu", "liste"]):
            st.markdown('<div class="nutri-box">Nutri: Diyet listenize tam uygun menü:<br><br><b>Kahvalti:</b> Yulaf + meyve + yumurta (350 kcal)<br><b>Ogle:</b> Izgara balik + salata (400 kcal)<br><b>Aksam:</b> Sebze Corbasi + et (350 kcal)<br><b>Atistirma:</b> Bir avuc badem (150 kcal)<br><br><b>Toplam: ~1250 kcal</b> - Günlük hedefinin altinda kalirsin!</div>', unsafe_allow_html=True)
        
        elif "su" in prompt_lower:
            kalan = 8 - st.session_state.water_count
            st.markdown('<div class="nutri-box">Su cok onemli! Suan ' + str(st.session_state.water_count) + '/8 bardak. ' + str(kalan) + ' bardak daha ic!<br><br><b>Su artirma ipuclari:</b><br>- Her öğünden önce 1 bardak su<br>- L limon veya nane ekle tatlandir<br>- Yaninda bir su sisemiz tasi!</div>', unsafe_allow_html=True)
        
        elif "kalori" in prompt_lower:
            st.markdown('<div class="nutri-box">Nutri: Günlük kaloriniz:<br><br><b>Yogunla:</b> ' + str(st.session_state.calorie_today) + ' kcal<br><b>Hedef:</b> 2000 kcal<br><b>Kalan:</b> ' + str(max(0, 2000 - st.session_state.calorie_today)) + ' kcal<br><br>' + ('Harika gidiyorsun, hedefe yakinsin!' if st.session_state.calorie_today < 2000 else 'Dikkat! Hedefi astin ama hemen panik yok, yarin daha dikkatli ol!') + '</div>', unsafe_allow_html=True)
        
        elif "diyet" in prompt_lower or "plan" in prompt_lower:
            st.markdown('<div class="nutri-box">Nutri: Senin icin hazirlanan haftalik diyet listesi var!<br><br>Günleri yukaridan sec ve her öğünü gör.<br><br>Listen dışında bir sey yemek istersen, bana sor - alternatif önereyim!<br><br>Birlikte basaracagiz!</div>', unsafe_allow_html=True)
        
        else:
            st.markdown('<div class="nutri-box">Nutri: Merhaba! Sana yardimci olmak icin buradayim.<br><br>Sor bana:<br>- "Pilav yerine ne yiyebilirim?"<br>- "Bugun ne yemeliyim?"<br>- "Kalorim ne durumda?"<br>- "Su hatirlatması yap"<br><br>Her sorun icin yanindayim!</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div style="text-align:center;color:rgba(255,255,255,0.3);padding:30px;">(c) 2026 DiyetX - Nutri ile saglikli yasam!<br><small>Yapim: Emir Unsal Aksu</small></div>', unsafe_allow_html=True)
