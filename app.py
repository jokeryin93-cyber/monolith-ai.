import streamlit as st
import time

st.set_page_config(page_title="MONOLITH CONTROL", layout="centered")

# Дизайн кнопок и карточек
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    .status-card {
        background: #1c1f26; padding: 15px; border-radius: 20px; 
        border: 1px solid #30363d; text-align: center; margin-bottom: 10px;
    }
    /* Стиль для зеленой кнопки Старт */
    div.stButton > button:first-child { background-color: #00c853; color: white; border: none; }
    .bot-running { border-left: 5px solid #00c853; background: #1e2329; padding: 10px; border-radius: 8px; margin-bottom: 10px; }
    .bot-stopped { border-left: 5px solid #ff1744; background: #1e1e1e; padding: 10px; border-radius: 8px; margin-bottom: 10px; opacity: 0.6; }
    </style>
    """, unsafe_allow_html=True)

if 'active_bots' not in st.session_state:
    st.session_state.active_bots = {} # Храним состояние каждого бота

st.title("🛡️ MONOLITH AI CONTROL")

# 1. НАСТРОЙКИ НОВОЙ СЕССИИ
with st.expander("⚙️ НАСТРОИТЬ НОВОГО БОТА"):
    col1, col2 = st.columns(2)
    with col1:
        new_bot = st.selectbox("🤖 БОТ", ["Сипер тренд", "без убыт"])
        new_tf = st.selectbox("⏳ ТФ", ["M1", "M5", "M15", "H1"])
    with col2:
        new_sym = st.selectbox("📊 РЫНОК", ["XAUUSD", "BTCUSD"])
        new_lot = st.number_input("💰 ЛОТ", 0.01, 1.0, 0.01, 0.01)
    
    if st.button("➕ ДОБАВИТЬ В ПАНЕЛЬ"):
        bot_id = f"{new_bot}_{new_sym}"
        st.session_state.active_bots[bot_id] = {
            "name": new_bot, "sym": new_sym, "tf": new_tf, "lot": new_lot, "active": False
        }

st.divider()

# 2. ПАНЕЛЬ УПРАВЛЕНИЯ БОТАМИ
st.write("### ⚡ УПРАВЛЕНИЕ РОБОТАМИ")

if not st.session_state.active_bots:
    st.info("Добавьте бота через меню выше 👆")
else:
    for bot_id, data in list(st.session_state.active_bots.items()):
        # Определяем стиль в зависимости от того, включен бот или нет
        card_style = "bot-running" if data['active'] else "bot-stopped"
        status_icon = "🟢 LIVE" if data['active'] else "🔴 STOPPED"
        
        st.markdown(f"""
        <div class="{(card_style)}">
            <small>{status_icon}</small><br>
            <b>{data['name']}</b> | {data['sym']} | {data['tf']} | Лот: {data['lot']}
        </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3 = st.columns([2, 2, 1])
        
        with btn_col1:
            # Зеленая кнопка START
            if st.button(f"▶️ START", key=f"start_{bot_id}"):
                st.session_state.active_bots[bot_id]['active'] = True
                st.rerun()
        
        with btn_col2:
            # Кнопка STOP
            if st.button(f"⏹️ STOP", key=f"stop_{bot_id}"):
                st.session_state.active_bots[bot_id]['active'] = False
                st.rerun()
        
        with btn_col3:
            # Удалить бота из панели
            if st.button("🗑️", key=f"del_{bot_id}"):
                del st.session_state.active_bots[bot_id]
                st.rerun()

st.divider()
# Общие команды для MT5
st.button("🔴 ВЫКЛЮЧИТЬ ВСЁ (EMERGENCY STOP)")
