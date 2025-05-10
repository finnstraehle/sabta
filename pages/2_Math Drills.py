import streamlit as st
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from data.drill_questions import drill_questions

# ── Initial State ─────────────────────────────────────────────────────────────
if "stats" not in st.session_state:
    st.session_state.stats = {
        cat: {"attempted": 0, "correct": 0}
        for cat in [
            "Basic Math", "Real World Math", "Logical Reasoning",
            "Numerical Reasoning"
        ]
    }


def gen_basic_question(level):
    """Generate a random basic math question for given difficulty."""
    ops = ["+", "-"] if level == 1 else ["+", "-", "*"] if level == 2 else ["+", "-", "*", "/"]
    max_val = 20 if level == 1 else 50 if level == 2 else 100
    a = random.randint(1, max_val)
    b = random.randint(1, max_val)
    op = random.choice(ops)
    if op == "+":
        return f"{a} + {b}", a + b
    if op == "-":
        a, b = max(a,b), min(a,b)
        return f"{a} - {b}", a - b
    if op == "*":
        return f"{a} × {b}", a * b
    # division: ensure integer result
    result = random.randint(1, max_val//2)
    return f"{result*b} ÷ {b}", result

def get_question(category, level):
    """Return a (question, answer) tuple based on category."""
    if category == "Basic Math":
        return gen_basic_question(level or 1)
    data = drill_questions[category]
    if category == "Chart Analysis":
        series, q, ans = random.choice(data)
        return (series, q), ans
    return random.choice(data)

def check_answer(user, correct):
    """Validate user's answer against correct answer."""
    try:
        # numeric compare
        if isinstance(correct, (int, float)):
            return abs(float(user) - correct) < 1e-6
    except:
        pass
    return str(user).strip().lower() == str(correct).lower()

def clear_drill_state():
    """Remove all session state keys related to drills except stats."""
    stats = st.session_state.stats
    st.session_state.clear()
    st.session_state.stats = stats

# ── Page Setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Math Drills", layout="wide")
st.title("🧠 Practice Drills")

st.write("Solve timed drills. Press Enter to submit answers. After each drill you can start a new one.")

# Show overall stats
with st.expander("Your Overall Stats (in this session)"):
    df = {
        cat: {
            "attempted": v["attempted"],
            "correct": v["correct"],
            "accuracy (%)": round(v["correct"]/v["attempted"]*100) if v["attempted"]>0 else 0
        }
        for cat,v in st.session_state.stats.items()
    }
    st.table(df)

# ── Drill Setup ────────────────────────────────────────────────────────────────
if not st.session_state.get("drill_active"):
    cat = st.selectbox("Category:", list(drill_questions.keys()), key="cat_select")
    level = st.selectbox("Difficulty (Basic Math):", [1,2,3], format_func=lambda x:f"Level {x}") if cat=="Basic Math" else None
    mins = st.radio("Duration (minutes):", [1,2,3])
    if st.button("Start Drill"):
        st.session_state.update({
            "drill_active": True,
            "cat": cat,
            "level": level,
            "end_time": datetime.now()+timedelta(minutes=mins),
            "attempted":0,
            "correct":0,
            "current_q": None,
            "feedback": ""
        })
        st.rerun()

# ── Drill Execution ────────────────────────────────────────────────────────────
if st.session_state.get("drill_active"):
    now = datetime.now()
    if now >= st.session_state.end_time:
        # Drill ended
        a,t = st.session_state.correct, st.session_state.attempted
        st.success(f"Done! {a}/{t} correct ({round(a/t*100,1) if t else 0}%)")
        # update global stats
        sc = st.session_state.stats
        sc[st.session_state.cat]["attempted"] += t
        sc[st.session_state.cat]["correct"] += a
        if st.button("New Drill"):
            clear_drill_state()
            st.rerun()
    else:
        # Show timer
        remain = (st.session_state.end_time - now).seconds
        st.info(f"Time left: {remain//60:02d}:{remain%60:02d}")
        st.divider()
        # load question if needed
        if st.session_state.current_q is None:
            q,a = get_question(st.session_state.cat, st.session_state.level)
            st.session_state.current_q, st.session_state.current_a = q,a
            st.session_state.ans = ""
        # display question with styled container
        q = st.session_state.current_q
        # Display question with styled container
        if isinstance(q, tuple):
            series, question = q
            st.bar_chart(series)
        else:
            question = q

        with st.container():
            st.markdown(
            f"""
            <div style="padding: 20px; border: 2px solid #B0B0B0; border-radius: 10px; background-color: #F5F5F5;">
                <h2 style="color: #606060; text-align: center;">{question}</h2>
            </div>
            """,
            unsafe_allow_html=True
            )
        st.divider()
        # feedback
        if st.session_state.feedback:
            if "Correct" in st.session_state.feedback:
                st.success(st.session_state.feedback)
            else:
                st.error(st.session_state.feedback)
        # input
        ans = st.text_input("Answer (Enter to submit):", key="ans", on_change=lambda: st.session_state.update(submitted=True))
        # Early end button at bottom
        if st.button("End Drill Early", key="end_bottom"):
            st.session_state.end_time = datetime.now()
            st.rerun()
        if st.session_state.get("submitted"):
            correct = check_answer(st.session_state.ans, st.session_state.current_a)
            st.session_state.attempted += 1
            if correct:
                st.session_state.correct += 1
                st.session_state.feedback = "✅ Correct!"
            else:
                st.session_state.feedback = f"❌ Incorrect (Ans: {st.session_state.current_a})"
            # prepare next
            st.session_state.current_q = None
            st.session_state.submitted = False
            st.rerun()
