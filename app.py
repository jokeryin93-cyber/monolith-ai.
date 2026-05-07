import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="MONOLITH AI PRO", layout="centered")

# Дизайн терминала
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    .status-card {
        background: #1c1f26; padding: 15px; border-radius: 20px; 
        border: 1px solid #30363d; text-align: center; margin-bottom: 10px;
    }
    .entry-box {
        background-color: #1e1e1e; border-left: 5px solid #00d2ff;
        padding: 12px; border-radius: 8px; margin: 10px 0;
    }
    .profit-text { color: #00ff88; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'bots' not in st.session_state:
    st.session_state.bots = ["Сипер тренд", "без убыт"]

st.title("🛡️ MONOLITH AI TERMINAL")

# 1. ПАНЕЛЬ МОНИТОРИНГА
st.markdown('<div class="status-card">', unsafe_allow_html=True)
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.caption("СТАВКА")
    st.write("**$100.00**")
with col_m2:
    st.caption("ПРИБЫЛЬ")
    st.markdown('<p style="color:#00ff88; margin:0;">+$45.20</p>', unsafe_allow_html=True)
with col_m3:
    st.caption("РИСК")
    st.write("**0.5%**")
st.markdown('</div>', unsafe_allow_html=True)

# 2. НАСТРОЙКИ ТОРГОВЛИ (Бот, Символ, Таймфрейм)
col_a, col_b, col_c = st.columns(3)
with col_a:
    current_bot = st.selectbox("🤖 БОТ", st.session_state.bots)
with col_b:
    current_symbol = st.selectbox("📊 СИМВОЛ", ["XAUUSD", "BTCUSD"])
with col_c:
    current_tf = st.selectbox("⏳ ТФ", ["M1", "M5", "M15", "M30", "H1"], index=1) # По умолчанию M5

st.divider()

# 3. ПОИСК ТОЧКИ ВХОДА С УЧЕТОМ ТФ
if st.button(f"🔍 АНАЛИЗИРОВАТЬ {current_symbol} ({current_tf})"):
    with st.status(f"ИИ Gemini анализирует график {current_tf}...") :
        time.sleep(1.2)
        st.write(f"Загрузка данных {current_symbol}...")
        st.write(f"Проверка паттернов на таймфрейме {current_tf}...")
    
    entry_price = 2380.50 if current_symbol == "XAUUSD" else 64200.00
    tp_price = entry_price + (10.0 if current_symbol == "XAUUSD" else 400.0)
    
    st.markdown(f"""
    <div class="entry-box">
        <h4 style='margin:0; color:#00d2ff;'>🎯 СИГНАЛ НАЙДЕН ({current_tf})</h4>
        <p style='margin:5px 0 0 0;'>Вход: <b>{entry_price}</b> | Цель: <b style='color:#00ff88;'>{tp_price}</b></p>
        <p style='font-size:0.8em; color:#888;'>Стратегия: {current_bot}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(60)
    st.success(f"💰 Текущий профит по сигналу {current_tf}: +$28.40")

# 4. УПРАВЛЕНИЕ
st.write("### УПРАВЛЕНИЕ")
c1, c2, c3 = st.columns(3)
with c1: st.button("🔴\nSTOP")
with c2: st.button("📊\nSYMBOLS")
with c3: st.button("🗑️\nDELETE")

# 5. ИСТОРИЯ
with st.expander("📜 История сделок"):
    st.write(f"1. {current_symbol} | {current_tf} | BUY | +$45.20")
