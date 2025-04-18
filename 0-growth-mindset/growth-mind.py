import streamlit as st
import random
import time
from datetime import datetime

# ----------------- Setup -----------------
st.set_page_config(page_title="MotivaBoard", layout="centered")

# ----------------- Title -----------------
st.title("💖 MotivaBoard")
st.markdown(
    "<p style='font-size:26px; font-weight:bold; color:#4CAF50;'>Your Daily Dose of Motivation & Mindset</p>",
    unsafe_allow_html=True
)

# ----------------- Quotes -----------------
quotes = [
    "🌟 *Believe you can and you're halfway there.*",
    "🔥 *Don’t watch the clock; do what it does. Keep going.*",
    "🚀 *Push yourself, because no one else is going to do it for you.*",
    "💡 *It always seems impossible until it’s done.*",
    "🌈 *You are capable of amazing things.*"
]

affirmations = [
    "🌻 *I am strong, confident, and resilient.*",
    "✨ *I attract positivity and repel negativity.*",
    "🌞 *Each day is a new opportunity to grow.*",
    "💪 *I believe in myself and my ability to succeed.*",
    "🧠 *Challenges help me become stronger.*"
]

# ----------------- Show Random Quote with Green Line -----------------
st.subheader("💬 Random Quote")
if st.button("Inspire Me!"):
    selected_quote = random.choice(quotes)
    st.markdown(
        f"""
        <div style='
            border-left: 6px solid limegreen;
            background-color: rgba(200, 255, 200, 0.07);
            padding: 15px 10px;
            margin: 10px 0;
            font-size: 18px;
            font-weight: 500;
            color: #ffffff;
        '>{selected_quote}</div>
        """,
        unsafe_allow_html=True
    )


# ----------------- Daily Affirmation -----------------
st.subheader("🧘‍♀️ Daily Affirmation")
if st.button("Affirm Me!"):
    st.success(random.choice(affirmations))

# ----------------- Goals Checklist -----------------
st.subheader("🎯 Today's Goals")

goals = [
    "Finish one important task ✅",
    "Take a 5-minute mindful break 🧘‍♂️",
    "Read or learn something new 📚",
    "Help someone or be kind 💌",
    "Stay hydrated and take care of yourself 💧"
]

checked = []
for goal in goals:
    if st.checkbox(goal):
        checked.append(goal)

# ----------------- Gratitude Journal -----------------
st.subheader("📝 Gratitude Journal")
journal = st.text_area(
    "Write 1–3 things you're grateful for today:",
    placeholder="e.g., I'm grateful for my family, learning opportunities, and good health."
)

# ----------------- Submission -----------------
if st.button("Save My Positivity"):
    if journal.strip() == "":
        st.warning("🌤️ Please write something positive before saving.")
    else:
        with st.spinner("Saving your entry..."):
            time.sleep(1.5)
        st.success("🎉 Great job! Your mindset is your superpower 💥")
        st.balloons()

# ----------------- Footer -----------------
st.markdown("---")
st.info("💡 *Keep showing up for yourself. One small step each day leads to big change.*")
