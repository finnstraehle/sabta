import streamlit as st
import random
import time
# load our predefined set of sparring questions from the data folder
from data.sparring_questions import sparring_questions

# Set the page configuration for the Streamlit app, including title and layout style
st.set_page_config(
    page_title="Interview Sparring",
    page_icon="🥊",
    layout="wide"
)

# Sabta logo generated by ChatGPT using the following prompt:
# "Generate a logo for a consulting interview preparation platform called 'SABTA'. The logo should be modern, professional, and also have some details. Use a color palette that includes blue."
# OpenAI. (2025). ChatGPT (Version 4.o) [Large language model]. https://chatgpt.com
st.logo("data/sabta_logo.png", size="large")

st.title("🥊 Interview Sparring")

# initialize sparring_active in session state if not already set
if 'sparring_active' not in st.session_state or not st.session_state.sparring_active:
    st.session_state.sparring_active = False

    # display instructions explaining how the sparring session works
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

    # draw a visual divider between instructions and controls
    st.divider()

    # allow user to choose how many questions to practice
    nr_of_questions = st.slider("**How many questions would you like to answer?**", 1, 30, 10)

    # give the option to enable a countdown timer for each question
    use_timer = st.checkbox("**Use a Timer?**")
    if use_timer:
        # let user set the time limit per question if timer is enabled
        time_limit = st.slider("**How long would you like to answer each question? (Seconds)**", 10, 300, 100)

    # extract the list of available topics from the questions dictionary
    topics = list(sparring_questions.keys())
    # let the user select which topics to include in the session
    selected = st.multiselect(
        "**Select topics to practice:**",
        options=topics,
        key="sparring_topics_select"
    )

    # start the sparring session when the button is clicked
    if st.button("Start Sparring"):
        if not selected:
            st.warning("Please choose at least one topic.")
        else:
            # build a randomized queue of selected questions
            queue = [(topic, q) for topic in selected for q in sparring_questions[topic]]
            random.shuffle(queue)
            # store only the requested number of questions in session state
            st.session_state.sparring_queue = queue[:nr_of_questions]
            st.session_state.sparring_index = 0
            st.session_state.sparring_active = True
            st.session_state.time_limit = time_limit if use_timer else None
            st.rerun()

# if a session is active, show questions one by one
if st.session_state.get('sparring_active'):
    # get the current question index from session state
    idx = st.session_state.sparring_index
    queue = st.session_state.sparring_queue
    total_q = len(queue)

    # check if we have finished all questions
    if idx >= total_q:
        st.success("🎉 You've completed all selected questions!")
        if st.button("Restart Sparring"):
            st.session_state.sparring_active = False
            st.rerun()
    else:
        topic, question = queue[idx]
        # display the progress indicator and topic for the current question
        st.markdown(f"**Question {idx+1} of {total_q}**  •  _Topic: {topic}_")
        with st.container():
            # show the question text inside a styled HTML box
            # Div coded once in a seperate HTML file and then copied in to every page only changing the color
            st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #FF4B4B; border-radius: 10px; background-color: #FFF5F5;">
                <h2 style="color: #FF4B4B; text-align: center;">{question}</h2>
            </div>
            """,
            unsafe_allow_html=True
            )
        # prompt the user to verbally answer before clicking next
        st.write("_Answer aloud, then click below when ready._")

        # buttons to move to the next question or end the session early
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Next Question"):
                st.session_state.sparring_index += 1
                st.rerun()
        with col2:
            if st.button("End Session"):
                st.session_state.sparring_active = False
                st.rerun()

        # if timer is enabled, count down and update progress bar
        if st.session_state.time_limit:
            timer_placeholder = st.empty()
            progress_bar = st.progress(0)
            for remaining in range(st.session_state.time_limit, 0, -1):
                timer_placeholder.markdown(f"⏳ Time remaining: {remaining} seconds")
                progress_bar.progress((st.session_state.time_limit - remaining) / st.session_state.time_limit)
                time.sleep(1)
            timer_placeholder.markdown("⏳ Time's up!")
            progress_bar.progress(1.0)
