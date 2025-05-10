import streamlit as st
import random
import time
from openai import OpenAI
from dotenv import load_dotenv
import os
from data.sparring_questions import sparring_questions

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("Fehlender OpenAI API-Key. Bitte `.env` Datei erstellen mit `OPENAI_API_KEY=...`")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# Set page configuration and logo
st.set_page_config(
    page_title="Interview Sparring – AI Chatbot",
    page_icon="🤖",
    layout="wide"
)
st.logo("data/sabta_logo.png", size="large")

st.title("🤖 Interview Sparring – AI Chatbot")

# Sparring Settings
if 'sparring_active' not in st.session_state or not st.session_state.sparring_active:
    st.session_state.sparring_active = False

    st.write(
        "Simulate a rapid‑fire interview Q&A session. "
        "Select one or more topics below, click **Start**, then answer each question aloud. "
        "Click **Next Question** when you're ready to move on, or **End Session** to stop."
        " This is a great way to practice your verbal responses and get comfortable with the interview format."
        " You can also use this to practice with a friend or mentor."
        " The questions are categorized by topic, and you can choose to focus on specific areas or mix them up for a more varied experience."
        " The questions are designed to be challenging and thought-provoking, so don't worry if you don't know the answer right away."
        " Take your time to think through your response and articulate your thoughts clearly."
    )

    st.divider()

    topics = list(sparring_questions.keys())
    selected = st.multiselect(
        "**Select topics to practice:**",
        options=topics,
        key="sparring_topics_select"
    )
    
    # Fixed number of questions for sparring
    nr_of_questions = 3

    # Fixed timer: always 60 seconds per question
    time_limit = 60

    if st.button("Start Sparring"):
        if not selected:
            st.warning("Please choose at least one topic.")
        else:
            queue = [(topic, q) for topic in selected for q in sparring_questions[topic]]
            random.shuffle(queue)
            st.session_state.sparring_queue = queue[:nr_of_questions]
            st.session_state.sparring_index = 0
            st.session_state.sparring_active = True
            st.session_state.time_limit = time_limit
            st.rerun()

# Sparring Session
if st.session_state.get('sparring_active'):
    idx = st.session_state.sparring_index
    queue = st.session_state.sparring_queue
    total_q = len(queue)

    if idx >= total_q:
        st.success("🎉 You've completed all selected questions!")
        if st.button("Restart Sparring"):
            st.session_state.sparring_active = False
            st.rerun()
    else:
        topic, question = queue[idx]
        st.markdown(f"**Question {idx+1} of {total_q}**  •  _Topic: {topic}_")
        with st.container():
            st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #4B9BFF; border-radius: 10px; background-color: #F5F9FF;">
                <h2 style="color: #4B9BFF; text-align: center;">{question}</h2>
            </div>
            """,
            unsafe_allow_html=True
            )
        st.write("_Answer aloud, then click below when ready._")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Next Question"):
                st.session_state.sparring_index += 1
                st.rerun()
        with col2:
            if st.button("End Session"):
                st.session_state.sparring_active = False
                st.rerun()

        # Timer with Progress Bar
        if st.session_state.time_limit:
            timer_placeholder = st.empty()
            progress_bar = st.progress(0)
            for remaining in range(st.session_state.time_limit, 0, -1):
                timer_placeholder.markdown(f"⏳ Time remaining: {remaining} seconds")
                progress_bar.progress((st.session_state.time_limit - remaining) / st.session_state.time_limit)
                time.sleep(1)
            timer_placeholder.markdown("⏳ Time's up!")
            progress_bar.progress(1.0)
