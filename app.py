import streamlit as st
import time
import sqlite3

st.set_page_config(page_title="Velora AI", layout="wide")

st.title("🚀 Velora AI")

# -----------------------------
# DATABASE
# -----------------------------
conn = sqlite3.connect("velora.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    message TEXT
)
""")

conn.commit()

def save_message(role, msg):
    c.execute("INSERT INTO messages (role, message) VALUES (?, ?)", (role, msg))
    conn.commit()

def get_messages():
    c.execute("SELECT role, message FROM messages")
    return c.fetchall()

# -----------------------------
# SIMPLE AI (FREE MODE)
# -----------------------------
def fake_ai(prompt):
    return f"🤖 پاسخ ساده AI: {prompt}"

# -----------------------------
# SIDEBAR MENU
# -----------------------------
menu = st.sidebar.radio("Menu", ["Chat", "Study"])

# -----------------------------
# CHAT
# -----------------------------
if menu == "Chat":
    st.subheader("💬 AI Chat")

    msg = st.text_input("پیام خود را بنویس")

    if st.button("Send"):
        if msg:
            save_message("user", msg)
            response = fake_ai(msg)
            save_message("ai", response)

    msgs = get_messages()

    for role, m in msgs:
        if role == "user":
            st.write("🧑 شما:", m)
        else:
            st.write("🤖 Velora:", m)

# -----------------------------
# STUDY TIMER
# -----------------------------
elif menu == "Study":
    st.subheader("⏱ Study Mode")

    if "start" not in st.session_state:
        st.session_state.start = None

    if st.button("Start"):
        st.session_state.start = time.time()
        st.success("شروع شد")

    if st.button("Stop"):
        if st.session_state.start:
            elapsed = time.time() - st.session_state.start
            st.session_state.start = None
            st.success(f"زمان مطالعه: {int(elapsed)} ثانیه")
