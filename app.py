import streamlit as st
import random
import time
from quiz_data import quiz_bank as question_bank

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Smart Quiz App", layout="centered")

st.title("🧠 Smart Quiz App")
st.write("Test your knowledge in a fun and interactive way!")

st.markdown("### 👩‍💻 Created by Iqra & Imsal")
st.caption("A simple AI-style quiz system built without any API 🎓")


# ---------------- USER INPUT ----------------
selected_topic = st.selectbox("📘 Choose Subject", list(question_bank.keys()))
selected_level = st.selectbox("🎯 Select Difficulty", ["Easy", "Medium", "Hard"])

available_qs = question_bank[selected_topic][selected_level]
max_qs = len(available_qs)

st.info(f"📚 Currently we have {max_qs} questions in this category.")

total_questions = st.slider(
    "❓ Number of Questions",
    1,
    max_qs,
    min(5, max_qs)
)


# ---------------- SESSION STATE ----------------
if "quiz_set" not in st.session_state:
    st.session_state.quiz_set = []

if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

if "time_limit" not in st.session_state:
    st.session_state.time_limit = 0


# ---------------- CREATE QUIZ ----------------
def create_quiz():
    selected_questions = random.sample(available_qs, total_questions)

    # shuffle options ONCE only
    for q in selected_questions:
        shuffled = q["options"].copy()
        random.shuffle(shuffled)
        q["shuffled_options"] = shuffled

    st.session_state.quiz_set = selected_questions
    st.session_state.user_answers = {}
    st.session_state.start_time = time.time()
    st.session_state.quiz_finished = False
    st.session_state.time_limit = total_questions * 15


# ---------------- SCORE FUNCTION ----------------
def calculate_score():
    score = 0
    for i, q in enumerate(st.session_state.quiz_set):
        user_ans = st.session_state.user_answers.get(f"q{i}")
        if user_ans == q["answer"]:
            score += 1
    return score


# ---------------- START QUIZ ----------------
if st.button("🚀 Start Quiz"):
    if max_qs == 0:
        st.warning("No questions available.")
    else:
        create_quiz()
        st.success("Good luck! 🍀 Try your best!")


# ---------------- TIMER (OPTION 2 - STABLE VERSION) ----------------
if st.session_state.start_time and not st.session_state.quiz_finished:

    elapsed = time.time() - st.session_state.start_time

    # if time is over → auto submit
    if elapsed >= st.session_state.time_limit:
        st.session_state.quiz_finished = True
        st.warning("⛔ Time is over! Quiz submitted automatically.")
    else:
        st.info(f"⏳ Time Limit: {int(st.session_state.time_limit - elapsed)} seconds")


# ---------------- QUESTIONS ----------------
if st.session_state.quiz_set and not st.session_state.quiz_finished:
    st.subheader("📋 Answer the following questions:")

    for i, q in enumerate(st.session_state.quiz_set):
        st.write(f"**Q{i+1}: {q['question']}**")

        options = q["shuffled_options"]

        answer = st.radio(
            "Choose your answer:",
            options,
            key=f"q{i}"
        )

        st.session_state.user_answers[f"q{i}"] = answer

    if st.button("✅ Submit Quiz"):
        st.session_state.quiz_finished = True


# ---------------- RESULT ----------------
if st.session_state.quiz_finished and st.session_state.quiz_set:
    final_score = calculate_score()
    total = len(st.session_state.quiz_set)

    st.success(f"🎉 Your Score: {final_score} / {total}")

    if final_score == total:
        st.balloons()
        st.success("Excellent! Perfect score! 🌟")
    elif final_score >= total / 2:
        st.success("Great job! 👍")
    else:
        st.warning("Keep practicing 💪")


# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("👩‍💻 Developed by **Iqra & Imsal | Smart Quiz App Project**")