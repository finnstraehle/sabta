import streamlit as st
import random
import time
from data.sparring_questions import sparring_questions

st.set_page_config(page_title="Interview Sparring", layout="wide")

st.title("Interview Sparring")

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

    topics = list(sparring_questions.keys())
    selected = st.multiselect(
        "Select topics to practice:",
        options=topics,
        key="sparring_topics_select"
    )

    nr_of_questions = st.slider("How many questions would you like to answer?", 1, 30, 10)

    use_timer = st.checkbox("Use a Timer?")
    time_limit = 100  # Default time limit
    if use_timer:
        st.write("**Note:** The timer will count down from the time limit you set below.")
        time_limit = st.slider("How long would you like to answer each question? (Seconds)", 10, 300, 100)

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

            # Limit the queue to the number of questions defined by the user
            queue = queue[:nr_of_questions]

            st.session_state.sparring_queue = queue
            st.session_state.sparring_index = 0
            st.session_state.sparring_active = True
            st.session_state.time_limit = time_limit if use_timer else None
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
        st.write(f"> {question}")
        st.write("_Answer aloud, then click below when ready._")

        col1, col2 = st.columns(2)
        if col1.button("Next Question"):
            st.session_state.sparring_index += 1
            st.rerun()
        if col2.button("End Session"):
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
