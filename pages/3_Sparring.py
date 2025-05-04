import streamlit as st
import random
from data.sparring_questions import sparring_questions

# Audio and Text?
# Text to speech?
# AI reading?
# AI generated questions?
# Image?
# user chooses how many questions to answer
# timer
# timer for each question
# AI generated questions?


# Page Configuration
st.set_page_config(
    page_title="Interview Sparring",
    layout="wide"
)

st.title("Interview Sparring")
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

# ─── UI: Topic Selection ────────────────────────────────────────────────────────

if 'sparring_active' not in st.session_state or not st.session_state.sparring_active:
    st.session_state.sparring_active = False

    topics = list(sparring_questions.keys())
    selected = st.multiselect(
        "Select topics to practice:",
        options=topics,
        key="sparring_topics_select"
    )
    # Slider
    nr_of_questions = st.slider("How many Question would you like to answer?", 1, 30, 10)
    time_limit = st.slider("How long would you like to answer each question?", 10, 300, 100)


    if st.button("Start Sparring"):
        if not selected:
            st.warning("Please choose at least one topic.")
        else:
            # Build a shuffled queue of (topic, question)
            queue = []
            for topic in selected:
                for q in sparring_questions[topic]:
                    queue.append((topic, q))
            random.shuffle(queue)

            st.session_state.sparring_queue = queue
            st.session_state.sparring_index = 0
            st.session_state.sparring_active = True
            st.rerun()

# ─── UI: Sparring Session ─────────────────────────────────────────────────────

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
        st.write(f"> {question}")
        st.write("_Answer aloud, then click below when ready._")

        col1, col2 = st.columns(2)
        if col1.button("Next Question"):
            st.session_state.sparring_index += 1
            st.rerun()
        if col2.button("End Session"):
            st.session_state.sparring_active = False
            st.rerun()
