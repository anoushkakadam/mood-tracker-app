import streamlit as st
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import os

# Set up the page config before anything else
st.set_page_config(page_title="Mood Tracker", layout="centered")

# App description displayed at the very top
st.markdown("""
# 🧠 Mood Tracker

Welcome to the **Mood Tracker App**!

This tool is designed to help you log and visualize your daily moods over time.  
By selecting your current emotional state and logging it, you build a simple, personal mood history  
that can help you notice trends, reflect on your emotional well-being, and take small steps toward better mental health.

### Key Features:
- 📝 Log your mood with a single click  
- 📅 View your mood history anytime  
- 📊 Visualize your emotional trends with a frequency chart  

Whether you're feeling great or just getting through the day, tracking your moods is a small habit with big benefits.
""")

# Define moods and emojis
moods = {
    "Happy": "😊",
    "Sad": "😢",
    "Angry": "😠",
    "Tired": "😴",
    "Anxious": "😰",
    "Excited": "😄",
    "Relaxed": "😌"
}

log_file = "mood_log.txt"

# Log the selected mood
def log_mood(mood, emoji):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"{now} - Mood: {mood} {emoji}\n")

# Read the mood log
def read_log():
    if not os.path.exists(log_file):
        return "No log available yet."
    with open(log_file, "r", encoding="utf-8") as file:
        return file.read()

# Generate mood frequency chart
def plot_mood_chart():
    if not os.path.exists(log_file):
        st.warning("No mood data to display.")
        return

    with open(log_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    moods_logged = [line.split("Mood: ")[1].split()[0] for line in lines if "Mood:" in line]
    if not moods_logged:
        st.info("No moods recorded yet.")
        return

    mood_counts = Counter(moods_logged)

    fig, ax = plt.subplots()
    ax.bar(mood_counts.keys(), mood_counts.values(), color='skyblue')
    ax.set_title("Mood Frequency")
    ax.set_xlabel("Mood")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Mood logging section
st.markdown("---")
st.subheader("How are you feeling today?")
selected_mood = st.selectbox("Select your mood:", list(moods.keys()))
emoji = moods[selected_mood]

if st.button("Log Mood"):
    log_mood(selected_mood, emoji)
    st.success(f"Mood logged: {selected_mood} {emoji}")

# Mood log viewer
st.markdown("---")
st.subheader("📒 View Mood Log")
if st.button("Show Log"):
    log_data = read_log()
    st.text_area("Mood Log", log_data, height=300)

# Mood chart viewer
st.markdown("---")
st.subheader("📊 Mood Frequency Chart")
if st.button("Show Chart"):
    plot_mood_chart()
