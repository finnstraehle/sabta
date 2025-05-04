import streamlit as st
import random

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

st.title("🎤 Interview Sparring")
st.write(
    "Simulate a rapid‑fire interview Q&A session. "
    "Select one or more topics below, click **Start**, then answer each question aloud. "
    "Click **Next Question** when you're ready to move on, or **End Session** to stop."
)

# Question Bank
sparring_questions = {
    "Business - Basic": [
        "What are the 4 Ps of marketing?",
        "Define 'market segmentation'.",
        "Explain the difference between revenue and profit.",
        "What does 'MECE' stand for and why is it important?",
        "How would you assess whether a product launch was successful?"
    ],
    "Business - Advanced": [
        "Walk me through a Porter’s Five Forces analysis for the airline industry.",
        "How would you value a high‑growth startup with no profits?",
        "Explain how you would structure an M&A due‑diligence process.",
        "Discuss the pros and cons of vertical integration for a manufacturer.",
        "How do you evaluate the competitive advantage of a market leader?"
    ],
    "Economics - Basic": [
        "What is GDP and how is it calculated?",
        "Explain the law of supply and demand.",
        "What causes inflation?",
        "Define 'opportunity cost'.",
        "How does a price ceiling affect a market?"
    ],
    "Economics - Advanced": [
        "Explain the Phillips Curve and its implications.",
        "What is quantitative easing and when is it used?",
        "Discuss the trade‑off between inflation and unemployment.",
        "How do exchange rates affect a country’s exports?",
        "Explain the concept of 'moral hazard' in banking."
    ],
    "Finance - Basic": [
        "What is the time value of money?",
        "Explain the difference between simple and compound interest.",
        "How do you calculate ROI?",
        "Define 'liquidity'.",
        "What is a balance sheet?"
    ],
    "Finance - Advanced": [
        "Walk me through a DCF valuation step by step.",
        "What is IRR and how do you interpret it?",
        "Explain the impact of leverage on a company's ROE.",
        "How do you assess credit risk?",
        "What are the main components of a cash flow statement?"
    ],
    "Brain Teasers": [
        "Why are manhole covers round?",
        "How many golf balls can you fit in a school bus?",
        "You have 8 balls, one is heavier. How find it in 2 weighings?",
        "What is the angle between the hour and minute hands at 3:15?",
        "A snail climbs 3m up a wall by day, slips 2m at night. How long to reach 10m?"
    ],
    "Punches": [
        "Explain a complex topic you know in under 30 seconds.",
        "What’s your biggest weakness—and how are you fixing it?",
        "Sell me this pen.",
        "How many windows are in New York City?",
        "Describe a time you failed and what you learned."
    ],
    "Personal Fit - CV": [
        "Walk me through your resume.",
        "What are the top three things that aren’t on your resume?",
        "Why did you choose your undergraduate major?",
        "How has your military background prepared you for consulting?",
        "Tell me about a gap or change in your CV."
    ],
    "Personal Fit - Why": [
        "Why consulting?",
        "Why our firm?",
        "Why now and not later?",
        "Why should we hire you over other candidates?",
        "Why did you leave your last role?"
    ],
    "Personal Fit - Situations": [
        "Tell me about a time you led a team under pressure.",
        "Describe a conflict you had to resolve at work.",
        "Give an example of when you had to influence without authority.",
        "Tell me about a time you made a decision with incomplete data.",
        "Describe a project that failed and how you responded."
    ],
    "Personal Fit - Tricky": [
        "If you could be any animal, which would you choose and why?",
        "How many slices of pizza are eaten in New York City each day?",
        "If I gave you $1 million to start a business, what would you do?",
        "How would you design an evacuation plan for this building?",
        "Sell me this app in 15 seconds."
    ]
}

# ─── UI: Topic Selection ────────────────────────────────────────────────────────

if 'sparring_active' not in st.session_state or not st.session_state.sparring_active:
    st.session_state.sparring_active = False

    topics = list(sparring_questions.keys())
    selected = st.multiselect(
        "Select topics to practice:",
        options=topics,
        key="sparring_topics_select"
    )

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
