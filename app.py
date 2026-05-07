import streamlit as st

st.set_page_config(page_title="MONOLITH AI", layout="centered")

# Дизайн
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    .status-card {
        background: #1c1f26; padding: 15px; border-radius: 20px; 
        border: 1px solid #30363d; text-align: center; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'bots' not in st.session_state:
    st.session_state.bots = ["Сипер тренд", "без убыт"]

st.title("🛡️ MONOLITH AI TERMINAL")

# ВЫБОР БОТА И СИМВОЛА
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("🤖 **РОБОТ**")
    current_bot = st.selectbox("Бот", st.session_state.bots, label_visibility="collapsed")
with col_b:
    st.markdown("📊 **СИМВОЛ**")
    current_symbol = st.selectbox("Символ", ["XAUUSD (Gold)", "BTCUSD (Crypto)"], label_visibility="collapsed")

st.markdown(f'''
<div class="status-card">
    <b>Активен:</b> {current_bot}<br>
    <b>Рынок:</b> {current_symbol}<br>
    🟢 Связь с Gemini: OK
</div>
''', unsafe_allow_html=True)

# КНОПКИ УПРАВЛЕНИЯ
c1, c2, c3 = st.columns(3)
with c1: st.button("🔴\nSTOP")
with c2: st.button("📊\nSYMBOLS")
with c3: st.button("🗑️\nDELETE")

st.divider()

# УПРАВЛЕНИЕ БОТАМИ
new_bot = st.text_input("Имя нового робота:", placeholder="Например: Scalper_V3")
if st.button("➕ ДОБАВИТЬ РОБОТА"):
    if new_bot and new_bot not in st.session_state.bots:
        st.session_state.bots.append(new_bot)
        st.rerun()

# ЗАПУСК АНАЛИЗА
if st.button(f"🚀 АНАЛИЗИРОВАТЬ {current_symbol.split()[0]}"):
    st.warning(f"ИИ Gemini проверяет {current_symbol} для стратегии {current_bot}...")
    # Здесь ИИ выдает сигнал
    st.success(f"🤖 Сигнал: Найдена точка входа на {current_symbol.split()[0]}!")
