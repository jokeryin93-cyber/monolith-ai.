import streamlit as st

st.set_page_config(page_title="MONOLITH AI ADMIN", layout="centered")

# Красивый дизайн как в мобильном приложении
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 12px; height: 55px; font-weight: bold; border: 1px solid #30363d; }
    .add-btn>div>button { background-color: #00d2ff; color: black; border: none; }
    .status-card {
        background: #1c1f26; padding: 20px; border-radius: 20px; 
        border: 1px solid #30363d; text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Инициализация списка ботов в памяти сессии
if 'bots' not in st.session_state:
    st.session_state.bots = ["SafeScalper_Pro (GOLD)", "Crypto_Matrix (BTC)"]

st.title("🛡️ MONOLITH AI")

# Блок выбора текущего бота
st.markdown("### 🤖 АКТИВНЫЙ РОБОТ")
current_bot = st.selectbox("", st.session_state.bots, label_visibility="collapsed")

st.markdown(f'<div class="status-card"><b>Выбран:</b> {current_bot}<br>🟢 Система готова к работе</div>', unsafe_allow_html=True)

# Кнопки управления (как на скрине)
c1, c2, c3 = st.columns(3)
with c1: st.button("🔴\nSTOP")
with c2: st.button("📊\nSYMBOLS")
with c3: st.button("🗑️\nDELETE")

st.divider()

# ФУНКЦИЯ ДОБАВЛЕНИЯ НОВОГО БОТА (то, что ты просил)
st.markdown("### ➕ УПРАВЛЕНИЕ")
new_bot_name = st.text_input("Введите имя нового робота:", placeholder="Например: AI_Scalper_V3")

if st.button("➕ ADD NEW ROBOT"):
    if new_bot_name:
        if new_bot_name not in st.session_state.bots:
            st.session_state.bots.append(new_bot_name)
            st.success(f"Робот {new_bot_name} добавлен в список!")
            st.rerun() # Обновляем страницу, чтобы бот появился в списке
    else:
        st.error("Сначала введите имя!")

# Кнопка запуска анализа
if st.button(f"🚀 ЗАПУСТИТЬ АНАЛИЗ {current_bot.split()[0]}"):
    st.info(f"ИИ Gemini начал сканирование для {current_bot}...")
