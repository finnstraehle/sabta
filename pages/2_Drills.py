# pages/2_Drills.py

import streamlit as st
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Practice Drills", page_icon="⏱️")

st.title("Practice Drills")
st.write(
    "Hone your skills with **timed drills**. Select a category and time limit, then solve as many questions as you can. "
    "Press **Enter** to submit each answer. Your answers will be checked instantly, and a score will be shown at the end."
)

# Question banks for fixed categories
real_world_questions = [
    ("If a bank offers 5% annual interest on $1,000, how much will you have after 1 year?", 1050),
    ("A company’s revenue is $500 and profit is $100. What is the profit margin (in %)?", "20%"),
    ("Fixed costs are $1,000 and profit per unit is $50. How many units must be sold to break even?", 20),
    ("If an investment grows from $200 to $242 in one year, what was the percentage gain?", "21%"),
    ("You invest $100 today and get $150 back in 3 years. What is the total return in dollars?", 50),
]
logical_questions = [
    ("If all VIPs are club members, and all club members are invited, are all VIPs invited? (True/False)", "True"),
    ("If A > B and B > C, is A > C? (True/False)", "True"),
    ("Tom is taller than Jim, and Jim is taller than Alex. Is Tom taller than Alex? (True/False)", "True"),
    ("All cats are mammals. Rex is a mammal. Conclusion: Rex is a cat. (True/False/Cannot Say)", "Cannot Say"),
    ("If the day after tomorrow is Friday, what day is today?", "Wednesday"),
]
numerical_questions = [
    ("If 5 pens cost $15, how much would 8 pens cost?", 24),
    ("A shop sells 3 apples for $1. How many apples can you buy for $5?", 15),
    ("There are 120 students, 55% of them are male. How many females are there?", 54),
    ("Train A travels 60 miles in 1 hour. How long to travel 150 miles at the same speed?", 2.5),
    ("A recipe needs 3 cups of flour to serve 4 people. How many cups are needed for 6 people?", 4.5),
]
chart_questions = [
    {"labels": ["Q1", "Q2", "Q3", "Q4"], "data": [10, 15, 5, 20],
     "question": "Which quarter had the highest sales?", "answer": "Q4"},
    {"labels": ["Q1", "Q2", "Q3", "Q4"], "data": [30, 20, 10, 15],
     "question": "Were sales highest in Q1? (True/False)", "answer": "True"},
]
verbal_questions = [
    ("\"All dogs have tails. Rex is a dog. Rex has a tail.\" Is this conclusion true? (True/False)", "True"),
    ("\"Some books are long. The Bible is a book. The Bible is long.\" Does this conclusion follow? (True/False/Cannot Say)", "Cannot Say"),
    ("If \"None of the engineers are women\" is true, can \"Some women are engineers\" be true? (True/False)", "False"),
    ("\"All A are B. All B are C. Therefore, all A are C.\" Is this conclusion valid? (True/False)", "True"),
    ("\"Most people have cats. John is a person. John has a cat.\" Does this conclusion follow? (True/False/Cannot Say)", "Cannot Say"),
]

def generate_basic_math_question(difficulty=1):
    """Generate a basic math question (adaptive difficulty)."""
    if difficulty == 1:
        ops, max_val = ['+', '-'], 20
    elif difficulty == 2:
        ops, max_val = ['+', '-', '*'], 50
    else:
        ops, max_val = ['+', '-', '*', '/'], 100

    op = random.choice(ops)
    if op == '+':
        a, b = random.randint(1, max_val), random.randint(1, max_val)
        return f"{a} + {b}", a + b
    if op == '-':
        a, b = random.randint(1, max_val), random.randint(1, max_val)
        if b > a: a, b = b, a
        return f"{a} - {b}", a - b
    if op == '*':
        limit = 10 if difficulty == 2 else 12
        a, b = random.randint(2, limit), random.randint(2, limit)
        return f"{a} * {b}", a * b
    # division
    b = random.randint(2, 12)
    result = random.randint(1, 10)
    return f"{b * result} / {b}", result

def check_answer(user_input, correct_answer):
    """Compare user_input (string) to correct_answer (int/float/str)."""
    if user_input is None: return False
    ui = user_input.strip().lower()
    # Numeric compare
    try:
        if isinstance(correct_answer, (int, float)):
            return abs(float(ui) - float(correct_answer)) < 1e-6
    except:
        pass
    ca = str(correct_answer).lower()
    if ca in ["true", "false", "cannot say"]:
        return ui == ca or (ca == "cannot say" and ui in ["can't say", "cannot say"])
    # percentage style
    return ui.replace("%","") == ca.replace("%","")

# ── Drill Setup ────────────────────────────────────────────────────────────────
if not st.session_state.get("drill_active", False):
    st.session_state.drill_active = False
    st.session_state.feedback_message = ""
    category = st.selectbox(
        "Choose a category:",
        ["Basic Math", "Real World Math", "Logical Reasoning",
         "Numerical Reasoning", "Chart Analysis", "Verbal Reasoning"],
        key="drill_category_select"
    )
    duration = st.radio("Time limit:", [3,5], format_func=lambda x: f"{x} minutes", key="drill_time_select")
    if st.button("Start Drill"):
        st.session_state.drill_active = True
        st.session_state.drill_category = category
        st.session_state.drill_end_time = datetime.now() + timedelta(minutes=duration)
        st.session_state.drill_attempts = 0
        st.session_state.drill_correct = 0
        # Adaptive difficulty state
        st.session_state.drill_difficulty = 1 if category=="Basic Math" else None
        st.session_state.correct_streak = 0
        st.session_state.current_question = None
        st.session_state.current_answer = None
        st.session_state.submitted = False
        st.session_state.user_input = ""
        st.rerun()

# ── Drill Execution ────────────────────────────────────────────────────────────
if st.session_state.get("drill_active"):
    now = datetime.now()
    time_left = (st.session_state.drill_end_time - now).total_seconds()
    stop = st.button("Stop Early")

    if time_left <= 0 or stop:
        # End drill
        total = st.session_state.drill_attempts
        correct = st.session_state.drill_correct
        accuracy = total and correct/total*100 or 0
        st.success("⏰ Time's up!" if time_left<=0 else "⏹️ Drill stopped.")
        st.write(f"**You answered {correct}/{total} correctly.**  Accuracy: {accuracy:.1f}%")
        # Update global stats
        cat = st.session_state.drill_category
        if total>0:
            st.session_state.stats[cat]["attempted"] += total
            st.session_state.stats[cat]["correct"] += correct
        # Pie chart
        if total>0:
            fig, ax = plt.subplots()
            ax.pie([correct, total-correct],
                   labels=["Correct","Incorrect"],
                   autopct="%1.0f%%",
                   colors=["#4caf50","#f44336"])
            ax.axis("equal")
            st.pyplot(fig)
        if st.button("New Drill"):
            st.session_state.drill_active = False
            st.rerun()
    else:
        # Show timer
        m, s = divmod(int(time_left),60)
        st.info(f"Time Remaining: {m:02d}:{s:02d}")

        # Load or generate question
        if st.session_state.current_question is None:
            cat = st.session_state.drill_category
            if cat == "Basic Math":
                q, a = generate_basic_math_question(st.session_state.drill_difficulty)
            elif cat == "Real World Math":
                q, a = random.choice(real_world_questions)
            elif cat == "Logical Reasoning":
                q, a = random.choice(logical_questions)
            elif cat == "Numerical Reasoning":
                q, a = random.choice(numerical_questions)
            elif cat == "Chart Analysis":
                item = random.choice(chart_questions)
                q, a = item["question"], item["answer"]
                st.session_state.chart_labels, st.session_state.chart_data = item["labels"], item["data"]
            else:  # Verbal
                q, a = random.choice(verbal_questions)
            st.session_state.current_question = q
            st.session_state.current_answer = a
            st.session_state.feedback_message = ""

        # Display chart if needed
        if st.session_state.drill_category == "Chart Analysis":
            df = {lab: val for lab, val in zip(st.session_state.chart_labels, st.session_state.chart_data)}
            st.bar_chart(df)

        # Show question & last feedback
        st.write(f"**Question:** {st.session_state.current_question}")
        if st.session_state.feedback_message:
            if st.session_state.feedback_message.startswith("Correct"):
                st.success(st.session_state.feedback_message)
            else:
                st.error(st.session_state.feedback_message)

        # Handle answer input
        def on_submit():
            st.session_state.submitted = True
        st.text_input("Your answer (press Enter):",
                      key="user_input",
                      on_change=on_submit)

        if st.session_state.submitted:
            user_ans = st.session_state.user_input
            correct_ans = st.session_state.current_answer
            is_right = check_answer(user_ans, correct_ans)
            st.session_state.drill_attempts += 1
            if is_right:
                st.session_state.drill_correct += 1
                st.session_state.feedback_message = "✅ Correct!"
                # Adaptive difficulty for Basic Math
                if st.session_state.drill_category=="Basic Math":
                    st.session_state.correct_streak += 1
                    if st.session_state.correct_streak >= 3 and st.session_state.drill_difficulty < 3:
                        st.session_state.drill_difficulty += 1
                        st.session_state.correct_streak = 0
            else:
                st.session_state.feedback_message = f"❌ Incorrect — the answer was {correct_ans}"
                if st.session_state.drill_category=="Basic Math":
                    st.session_state.correct_streak = 0

            # Reset for next question
            st.session_state.current_question = None
            st.session_state.current_answer = None
            st.session_state.submitted = False
            st.session_state.user_input = ""
            st.rerun()
