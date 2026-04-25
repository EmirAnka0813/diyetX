"""
DiyetX - AI Destekli Diyet Uygulaması
Tüm Rakip Özellikleri + Nutri AI
"""

import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as time_module

st.set_page_config(page_title="DiyetX", page_icon="🥗", layout="wide")

# === CSS ===
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
</style>
""", unsafe_allow_html=True)

# === SESSION STATES ===
if 'step' not in st.session_state: st.session_state.step = 0
if 'name' not in st.session_state: st.session_state.name = ""
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

# === ONAİBOARD ===
if st.session_state.step == 0:
    st.markdown("<h1 style='text-align:center;color:white;'>🥗 DiyetX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:white;font-size:20px;'>Sağlıklı beslen, hedefine ulaş!</p>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;font-size:100px;'>🐱</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background:white;border-radius:30px;padding:40px;max-width:500px;margin:auto;'>
        <h2 style='color:#667eea;'>Hoş Geldin!</h2>
    """, unsafe_allow_html=True)
    
    st.session_state.name = st.text_input("Adın?", placeholder="Adını yaz...")
    st.session_state.current_weight = st.number_input("Mevcut kilo (kg)", 30, 200, 80)
    st.session_state.goal_weight = st.number_input("Hedef kilo (kg)", 30, 200, 75)
    st.selectbox("Aktivite seviyesi", ["Sedanter", "Hafif aktif", "Orta", "Çok aktif"])
    st.selectbox("Diyet tercihi", ["Serbest", "Düşük karbonhidrat", "Yüksek protein", "Vejetaryen"])
    
    if st.button("🚀 Başla!"):
        if st.session_state.name:
            st.session_state.step = 1
            st.session_state.badges = ["🎯 İlk Adım"]
            st.rerun()
    st.stop()

# === ANA SAYFA ===
elif st.session_state.step == 1:
    # Header
    st.markdown("""
    <div style='background:white;border-radius:20px;padding:20px;margin-bottom:20px;'>
        <h2 style='margin:0;color:#667eea;'>🥗 DiyetX</h2>
        <p style='margin:0;'>Hoş geldin, <b>{}</b>! 👋</p>
    </div>
    """.format(st.session_state.name), unsafe_allow_html=True)
    
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
        badges_str = " ".join(st.session_state.badges[:3]) if st.session_state.badges else "🎖️"
        st.markdown("""
        <div class='metric-card'>
            <span style='font-size:40px;'>🎖️</span>
            <p style='font-size:14px;'>{}</p>
            <p>Rozetler</p>
        </div>
        """.format(badges_str), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === NUTRİ MESAJ ===
    st.markdown("""
    <div class='nutri-box'>
        🐱 <b>Nutri:</b> "Merhaba {}! Bugün {} kcal yedin, {} bardak su içtin. 
        Hedefine {} kg kaldı! 💪"
    </div>
    """.format(
        st.session_state.name,
        st.session_state.calorie_today,
        st.session_state.water_count,
        st.session_state.current_weight - st.session_state.goal_weight
    ), unsafe_allow_html=True)
    
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
        yemek_adi = st.text_input("Yemek", placeholder="Örnek: Tavuk salatası")
    with col_y2:
        yemek_kalori = st.number_input("Kalori", 0, 2000, 200)
    with col_y3:
        yemek_tip = st.selectbox("Tür", ["Kahvaltı", "Öğle", "Akşam", "Atıştırmalık"])
    
    # Makro girişi
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        yemek_protein = st.number_input("Protein (g)", 0, 200, 20)
    with col_m2:
        yemek_carbs = st.number_input("Karbonhidrat (g)", 0, 300, 25)
    with col_m3:
        yemek_fat = st.number_input("Yağ (g)", 0, 100, 10)
    
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
    
    if st.button(f"➕ Ekle {renk_emoji}"):
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
        water_pct = min(st.session_state.water_count / 8 * 100, 100)
        st.progress(water_pct, text=f"{st.session_state.water_count}/8 bardak")
        
        if st.button("💧 Su İçtim!", key="water"):
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
        new_steps = st.number_input("Adım ekle", 0, 50000, 1000)
        if st.button("👟 Adım Ekle"):
            st.session_state.steps += new_steps
            st.session_state.points += 5
            st.rerun()
    
    with col_a2:
        st.metric("Uyku", f"{st.session_state.sleep_hours}h", "saat / 8")
        new_sleep = st.slider("Uyku saati", 0, 12, 7)
        if st.button("😴 Uyku Kaydet"):
            st.session_state.sleep_hours = new_sleep
            if new_sleep >= 7:
                st.session_state.badges.append("😴 İyi Uyku")
                st.session_state.points += 20
            st.rerun()
    
    st.markdown("---")
    
    # === INTERMITTENT FASTING ===
    st.markdown("### ⏰ Intermittent Fasting")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fasting_plan = st.selectbox("Fasting Planı", ["Seç", "16:8", "18:6", "20:4", "5:2"])
        
        if not st.session_state.fasting_active:
            if st.button("▶️ Oruç Başlat"):
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
            
            if st.button("⏹️ Orucu Bitir"):
                st.session_state.fasting_active = False
                st.session_state.points += 50
                st.session_state.badges.append("⏰ Oruç Tamamlandı")
                st.success("Oruç tamamlandı! +50 puan 🎉")
                st.rerun()
    
    with col_f2:
        st.markdown("#### 🕐 Öğün Hatırlatıcıları")
        for i, reminder in enumerate(st.session_state.meal_reminders):
            st.write(f"• {reminder}")
        
        new_reminder = st.text_input("Hatırlatıcı ekle", placeholder="Örnek: 08:00 - Kahvaltı")
        if st.button("🔔 Ekle") and new_reminder:
            st.session_state.meal_reminders.append(new_reminder)
            st.rerun()
    
    st.markdown("---")
    
    # === DUYGUSAL YEME GÜNLÜĞÜ ===
    st.markdown("### 🧠 Duygusal Yeme Günlüğü (Noom Tarzı)")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        mood = st.selectbox("Şu anki ruh halin?", ["Mutlu", "Üzgün", "Stresli", "Sıkılmış", "Yorgun", "Endişeli"])
        if st.button("📝 Kaydet"):
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
    
    if prompt := st.text_input("Nutri'ye sor:", placeholder="Örnek: Bugün ne yemeliyim?"):
        
        if any(x in prompt.lower() for x in ["yemel", "ne yem", "yemek"]):
            st.markdown("""
            <div class='nutri-box'>
                <b>Nutri:</b> "{} için harika! 🍳
                Kahvaltı: Yulaf + meyve + yumurta (350 kcal)
                Öğle: Izgara tavuk + salata (450 kcal)
                Akşam: Fırında somon + sebze (400 kcal)
                💧 Arada 2 bardak su iç!"
            </div>
            """.format(st.session_state.name), unsafe_allow_html=True)
        elif "su" in prompt.lower():
            kalan = 8 - st.session_state.water_count
            st.markdown("""
            <div class='nutri-box'>
                <b>Nutri:</b> "{} su çok önemli! 💧 
                Şu an {}/8 bardak. {} bardak daha iç! 💪"
            </div>
            """.format(st.session_state.name, st.session_state.water_count, kalan), unsafe_allow_html=True)
        elif "oruç" in prompt.lower() or "fasting" in prompt.lower():
            st.markdown("""
            <div class='nutri-box'>
                <b>Nutri:</b> "Intermittent fasting harika! ⏰
                16:8 = 16 saat oruç, 8 saat yemek
                18:6 = 18 saat oruç, 6 saat yemek
                Hangisini tercih edersin? 😊"
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='nutri-box'>
                <b>Nutri:</b> "Harika soru {}! 😊 
                Sana yardımcı olmak için buradayım!"
            </div>
            """.format(st.session_state.name), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # === BMR HESAPLAYICI ===
    st.markdown("### 🧮 BMR Hesaplayıcı")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        age = st.number_input("Yaş", 10, 100, 25)
        height_cm = st.number_input("Boy (cm)", 120, 220, 170)
        weight_kg = st.number_input("Kilo (kg)", 30, 200, st.session_state.current_weight)
        
        if st.button("📊 BMR Hesapla"):
            # Mifflin-St Jeor
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
            st.session_state.bmr = bmr
            st.success(f"Bazal Metabolizma Hızın: {bmr} kcal/gün")
    
    with col_b2:
        if 'bmr' in st.session_state:
            bmr_val = st.session_state.bmr
            st.markdown("""
            <div class='metric-card'>
                <h3>BMR: {} kcal/gün</h3>
                <p>Günde {} kcal tüketirsen kilo verirsin</p>
            </div>
            """.format(bmr_val, bmr_val - 500), unsafe_allow_html=True)
    
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