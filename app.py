import streamlit as st

# Настройка мобильного вида
st.set_page_config(page_title="MONOLITH AI", layout="centered")

# Дизайн как на твоем скриншоте
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #121212; }
    .stButton>button { 
        width: 100%; border-radius: 15px; height: 70px; 
        font-weight: bold; font-size: 18px; text-transform: uppercase;
    }
    .status-card {
        background: linear-gradient(145deg, #1e1e1e, #252525);
        padding: 20px; border-radius: 20px; border: 1px solid #333;
        text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Заголовок и карточка робота
st.markdown('<div class="status-card">', unsafe_allow_html=True)
st.image("https://img.icons8.com/fluency/96/robot-3.png", width=80)
st.subheader("MONOLITH SCALPER AI")
st.write("🛡️ Статус: Работает | 📊 XAUUSD")
st.markdown('</div>', unsafe_allow_html=True)

# Кнопки управления (как на скрине)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔴\nSTOP"): st.error("Остановлен")
with col2:
    if st.button("📊\nSYMBOLS"): st.info("Gold / Crypto")
with col3:
    if st.button("🗑️\nDELETE"): st.warning("Очистка")

# Большая кнопка запуска
if st.button("🚀 ЗАПУСТИТЬ ИИ-АНАЛИЗ"):
    st.success("🤖 Gemini: Вижу точку входа на покупку (BUY)!")
