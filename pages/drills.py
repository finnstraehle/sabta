import IPython
import streamlit as st
import random
import time

def drills_page():
    """
    This page is fully fleshed out with two main categories:
    1) Basic Math
    2) Real-World Math

    Users can select a subcategory, choose a time limit (3 or 5 minutes),
    and start a timed drill. Once the drill starts, the app automatically
    generates questions, validates answers, and moves to the next question
    without extra button clicks (user presses Enter to submit).

    At the end of the time limit, the user sees their score and attempts.
    """

    st.title("Drills")
    st.write("Practice your math and real-world problem-solving skills under time pressure.")

    # Initialize default session state values if they don't exist
    if "drill_in_progress" not in st.session_state:
        st.session_state.drill_in_progress = False
    if "category" not in st.session_state:
        st.session_state.category = None
    if "subcategory" not in st.session_state:
        st.session_state.subcategory = None
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0
    if "time_limit" not in st.session_state:
        st.session_state.time_limit = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "current_question" not in st.session_state:
        st.session_state.current_question = ("", None)  # (question_text, answer_value)
    if "last_feedback" not in st.session_state:
        st.session_state.last_feedback = ""  # To display "Correct!" or "Incorrect" momentarily
    if "drill_input" not in st.session_state:
        st.session_state.drill_input = ""

    # If a drill is not in progress, show the setup interface
    if not st.session_state.drill_in_progress:
        show_drill_setup()
    else:
        run_drill()


def show_drill_setup():
    """
    Displays the setup for the drill:
    - Choose Basic Math or Real-World Math
    - Choose subcategory (e.g., Addition, IRR, etc.)
    - Choose time limit (3 or 5 minutes)
    - Start the drill
    """
    st.subheader("Drill Setup")

    # Two main categories displayed side by side for clarity
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Basic Math")
        st.write("- Addition\n- Subtraction\n- Multiplication\n- Division\n- Percentages")

    with col2:
        st.markdown("### Real-World Math")
        st.write("""
        - Interest Rates
        - Growth Rates
        - CAGR
        - IRR
        - Payback Period
        - Break Even
        - Profit Margins
        - EBITDA
        """)

    st.write("**Select Your Drill Preferences**")
    st.session_state.category = st.selectbox(
        "Category",
        ["Basic Math", "Real-World Math"],
        index=0
    )

    # Based on the chosen category, load appropriate subcategories
    if st.session_state.category == "Basic Math":
        subcategories = [
            "Addition",
            "Subtraction",
            "Multiplication",
            "Division",
            "Percentages",
            "All Basic Math"
        ]
    else:  # Real-World Math
        subcategories = [
            "Interest Rates",
            "Growth Rates",
            "CAGR",
            "IRR",
            "Payback Period",
            "Break Even",
            "Profit Margins",
            "EBITDA",
            "All Real-World Math"
        ]

    st.session_state.subcategory = st.selectbox("Subcategory", subcategories)

    time_choice = st.radio("Time Limit", ["3 minutes", "5 minutes"])
    if time_choice == "3 minutes":
        chosen_limit = 180  # seconds
    else:
        chosen_limit = 300  # seconds

    # Button to start the drill
    if st.button("Start Drill"):
        # Initialize or reset session state variables
        st.session_state.drill_in_progress = True
        st.session_state.time_limit = chosen_limit
        st.session_state.start_time = time.time()
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.last_feedback = ""
        st.session_state.drill_input = ""

        # Generate the first question
        st.session_state.current_question = generate_question(
            st.session_state.category,
            st.session_state.subcategory
        )
        st.rerun()


def run_drill():
    """
    Manages the active drill session:
    - Checks if time is up
    - Displays the current question
    - Provides an input box for the user
    - Validates user input automatically (no extra clicks)
    - Generates a new question until time runs out
    """
    time_left = st.session_state.time_limit - (time.time() - st.session_state.start_time)

    if time_left <= 0:
        # Time is up; end the drill
        end_drill()
        return

    # Show time remaining
    minutes_left = int(time_left // 60)
    seconds_left = int(time_left % 60)
    st.info(f"Time Remaining: {minutes_left}m {seconds_left}s")

    # Display the last feedback (Correct/Incorrect) briefly
    if st.session_state.last_feedback:
        st.write(st.session_state.last_feedback)

    # Display the current question
    question_text, _ = st.session_state.current_question
    st.write(f"**Question:** {question_text}")

    # Text input that triggers a callback when user presses Enter
    # We'll store the user's input in session_state["drill_input"]
    st.text_input(
        "Your Answer (Press Enter to submit)",
        key="drill_input",
        on_change=check_drill_answer
    )


def check_drill_answer():
    """
    Callback function triggered whenever the user presses Enter in the text input.
    - Compares the input with the correct answer
    - Updates score/attempts
    - Generates a new question
    - Clears the input box
    - Checks time again
    """
    user_input = st.session_state.drill_input
    correct_answer = st.session_state.current_question[1]

    # If user typed nothing, just return (avoid infinite loop)
    if not user_input.strip():
        return

    # Increase attempts count
    st.session_state.attempts += 1

    # Check correctness
    try:
        # Compare float values for numeric answers
        if abs(float(user_input) - float(correct_answer)) < 0.001:
            st.session_state.score += 1
            st.session_state.last_feedback = "✅ Correct!"
        else:
            st.session_state.last_feedback = f"❌ Incorrect! The correct answer was {correct_answer}"
    except ValueError:
        # If we couldn't convert to float, treat it as incorrect
        st.session_state.last_feedback = f"❌ Incorrect format. The correct answer was {correct_answer}"

    # Generate the next question
    st.session_state.current_question = generate_question(
        st.session_state.category,
        st.session_state.subcategory
    )

    # Clear the input box
    st.session_state.drill_input = ""

    # Force a rerun to refresh the question and time
    st.rerun()


def end_drill():
    """
    Ends the drill session and shows the final results.
    Resets the 'drill_in_progress' flag so user can start a new drill if desired.
    """
    st.session_state.drill_in_progress = False
    st.success("Time is up!")
    st.write(f"**Total Attempts:** {st.session_state.attempts}")
    st.write(f"**Correct Answers:** {st.session_state.score}")

    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"**Accuracy:** {accuracy:.1f}%")
    else:
        st.write("No attempts recorded.")

    st.session_state.last_feedback = ""
    st.session_state.drill_input = ""


def generate_question(category, subcategory):
    """
    Returns a tuple (question_text, correct_answer).
    If subcategory is "All Basic Math" or "All Real-World Math", pick randomly
    from the relevant subcategories. Otherwise, pick the specified subcategory.
    """
    if category == "Basic Math":
        # Potential subcategories
        subs = ["Addition", "Subtraction", "Multiplication", "Division", "Percentages"]
        if subcategory == "All Basic Math":
            chosen_sub = random.choice(subs)
        else:
            chosen_sub = subcategory
        return generate_basic_math(chosen_sub)
    else:
        # Real-World Math
        subs = [
            "Interest Rates",
            "Growth Rates",
            "CAGR",
            "IRR",
            "Payback Period",
            "Break Even",
            "Profit Margins",
            "EBITDA"
        ]
        if subcategory == "All Real-World Math":
            chosen_sub = random.choice(subs)
        else:
            chosen_sub = subcategory
        return generate_real_world_math(chosen_sub)


def generate_basic_math(sub):
    """
    Generates a random basic math question and its answer.
    """
    if sub == "Addition":
        a, b = random.randint(1, 100), random.randint(1, 100)
        return (f"{a} + {b}", a + b)
    elif sub == "Subtraction":
        a, b = random.randint(1, 100), random.randint(1, 100)
        if b > a:  # ensure non-negative
            a, b = b, a
        return (f"{a} - {b}", a - b)
    elif sub == "Multiplication":
        a, b = random.randint(1, 12), random.randint(1, 12)
        return (f"{a} * {b}", a * b)
    elif sub == "Division":
        # Ensure integer division
        divisor = random.randint(1, 12)
        quotient = random.randint(1, 12)
        dividend = divisor * quotient
        return (f"{dividend} / {divisor}", quotient)
    elif sub == "Percentages":
        percent = random.choice([10, 15, 20, 25, 30, 40, 50])
        base = random.randint(50, 300)
        return (f"What is {percent}% of {base}?", (percent/100)*base)
    else:
        # Default fallback
        return ("Error: Unknown Basic Math Subcategory", 0)


def generate_real_world_math(sub):
    """
    Generates a random real-world math question and its answer.
    These are simplified examples, but can be expanded with more realism.
    """
    if sub == "Interest Rates":
        # E.g. "What is the interest earned on principal P at r% for T years?"
        P = random.randint(1000, 5000)
        r = random.randint(1, 10)  # interest rate in %
        T = random.randint(1, 5)
        question = f"Simple interest on ${P} at {r}% for {T} years?"
        answer = (P * r * T) / 100
        return (question, answer)

    elif sub == "Growth Rates":
        # "Value grows from A to B in T years. What is the overall growth rate (in %)?"
        A = random.randint(50, 500)
        B = A + random.randint(1, 200)
        T = random.randint(1, 5)
        growth = ((B - A) / A) * 100  # total growth % (not annualized)
        question = f"Value grows from {A} to {B} in {T} years. What is the total growth rate (%)?"
        return (question, growth)

    elif sub == "CAGR":
        # "Initial A, final B, T years, what's the CAGR?"
        A = random.randint(100, 1000)
        B = A + random.randint(1, 2000)
        T = random.randint(1, 5)
        # CAGR formula = (B/A)^(1/T) - 1
        cagr = ((B/A) ** (1/T) - 1) * 100
        question = f"Initial {A}, final {B}, over {T} years. What is the CAGR (%)?"
        return (question, cagr)

    elif sub == "IRR":
        # Very simplified example with 2 cash flows only
        # "Invest X now, get Y after T years, what's the IRR?"
        X = random.randint(1000, 5000)
        T = random.randint(1, 5)
        Y = X + random.randint(1, 5000)
        # IRR is the r that satisfies: -X + (Y)/(1+r)^T = 0
        # We'll do a rough approximation for demonstration
        # IRR approx from (Y/X)^(1/T) - 1
        irr_approx = ((Y/X) ** (1/T) - 1) * 100
        question = f"Invest {X} now, receive {Y} in {T} years. Approx IRR (%)?"
        return (question, irr_approx)

    elif sub == "Payback Period":
        # "Cost C, yearly return R, how many years to break even?"
        C = random.randint(1000, 5000)
        R = random.randint(100, 1000)
        payback = round(C / R, 2)
        question = f"Project costs {C} and returns {R} per year. Payback period (years)?"
        return (question, payback)

    elif sub == "Break Even":
        # "Fixed cost F, variable cost v, price p, how many units to break even?"
        F = random.randint(500, 2000)
        v = random.randint(5, 20)
        p = v + random.randint(1, 15)
        # Break-even units = F / (p - v)
        be_units = round(F / (p - v), 2)
        question = f"Fixed cost={F}, var cost={v}, price={p}. Break-even units?"
        return (question, be_units)

    elif sub == "Profit Margins":
        # "Revenue R, Cost C, what's the profit margin in %?"
        R = random.randint(1000, 5000)
        C = random.randint(500, R)  # cost <= revenue
        profit = R - C
        margin = (profit / R) * 100
        question = f"Revenue={R}, Cost={C}. Profit margin (%)?"
        return (question, margin)

import streamlit as st
import random
import time

def drills_page():
    """
    This page is fully fleshed out with two main categories:
    1) Basic Math
    2) Real-World Math

    Users can select a subcategory, choose a time limit (3 or 5 minutes),
    and start a timed drill. Once the drill starts, the app automatically
    generates questions, validates answers, and moves to the next question
    without extra button clicks (user presses Enter to submit).

    At the end of the time limit, the user sees their score and attempts.
    """

    st.title("Drills")
    st.write("Practice your math and real-world problem-solving skills under time pressure.")

    # Initialize default session state values if they don't exist
    if "drill_in_progress" not in st.session_state:
        st.session_state.drill_in_progress = False
    if "category" not in st.session_state:
        st.session_state.category = None
    if "subcategory" not in st.session_state:
        st.session_state.subcategory = None
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0
    if "time_limit" not in st.session_state:
        st.session_state.time_limit = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0
    if "current_question" not in st.session_state:
        st.session_state.current_question = ("", None)  # (question_text, answer_value)
    if "last_feedback" not in st.session_state:
        st.session_state.last_feedback = ""  # To display "Correct!" or "Incorrect" momentarily
    if "drill_input" not in st.session_state:
        st.session_state.drill_input = ""

    # If a drill is not in progress, show the setup interface
    if not st.session_state.drill_in_progress:
        show_drill_setup()
    else:
        run_drill()


def show_drill_setup():
    """
    Displays the setup for the drill:
    - Choose Basic Math or Real-World Math
    - Choose subcategory (e.g., Addition, IRR, etc.)
    - Choose time limit (3 or 5 minutes)
    - Start the drill
    """
    st.subheader("Drill Setup")

    # Two main categories displayed side by side for clarity
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Basic Math")
        st.write("- Addition\n- Subtraction\n- Multiplication\n- Division\n- Percentages")

    with col2:
        st.markdown("### Real-World Math")
        st.write("""
        - Interest Rates
        - Growth Rates
        - CAGR
        - IRR
        - Payback Period
        - Break Even
        - Profit Margins
        - EBITDA
        """)

    st.write("**Select Your Drill Preferences**")
    st.session_state.category = st.selectbox(
        "Category",
        ["Basic Math", "Real-World Math"],
        index=0
    )

    # Based on the chosen category, load appropriate subcategories
    if st.session_state.category == "Basic Math":
        subcategories = [
            "Addition",
            "Subtraction",
            "Multiplication",
            "Division",
            "Percentages",
            "All Basic Math"
        ]
    else:  # Real-World Math
        subcategories = [
            "Interest Rates",
            "Growth Rates",
            "CAGR",
            "IRR",
            "Payback Period",
            "Break Even",
            "Profit Margins",
            "EBITDA",
            "All Real-World Math"
        ]

    st.session_state.subcategory = st.selectbox("Subcategory", subcategories)

    time_choice = st.radio("Time Limit", ["3 minutes", "5 minutes"])
    if time_choice == "3 minutes":
        chosen_limit = 180  # seconds
    else:
        chosen_limit = 300  # seconds

    # Button to start the drill
    if st.button("Start Drill"):
        # Initialize or reset session state variables
        st.session_state.drill_in_progress = True
        st.session_state.time_limit = chosen_limit
        st.session_state.start_time = time.time()
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.last_feedback = ""
        st.session_state.drill_input = ""

        # Generate the first question
        st.session_state.current_question = generate_question(
            st.session_state.category,
            st.session_state.subcategory
        )
        st.rerun()


def run_drill():
    """
    Manages the active drill session:
    - Checks if time is up
    - Displays the current question
    - Provides an input box for the user
    - Validates user input automatically (no extra clicks)
    - Generates a new question until time runs out
    """
    time_left = st.session_state.time_limit - (time.time() - st.session_state.start_time)

    if time_left <= 0:
        # Time is up; end the drill
        end_drill()
        return

    # Show time remaining
    minutes_left = int(time_left // 60)
    seconds_left = int(time_left % 60)
    st.info(f"Time Remaining: {minutes_left}m {seconds_left}s")

    # Display the last feedback (Correct/Incorrect) briefly
    if st.session_state.last_feedback:
        st.write(st.session_state.last_feedback)

    # Display the current question
    question_text, _ = st.session_state.current_question
    st.write(f"**Question:** {question_text}")

    # Text input that triggers a callback when user presses Enter
    st.text_input(
        "Your Answer (Press Enter to submit)",
        key="drill_input",
        on_change=check_drill_answer
    )


def check_drill_answer():
    """
    Callback function triggered whenever the user presses Enter in the text input.
    - Compares the input with the correct answer
    - Updates score/attempts
    - Generates a new question
    - Clears the input box
    - Checks time again
    """
    user_input = st.session_state.drill_input
    correct_answer = st.session_state.current_question[1]

    # If user typed nothing, just return (avoid infinite loop)
    if not user_input.strip():
        return

    # Increase attempts count
    st.session_state.attempts += 1

    # Check correctness
    try:
        # Compare float values for numeric answers
        if abs(float(user_input) - float(correct_answer)) < 0.001:
            st.session_state.score += 1
            st.session_state.last_feedback = "✅ Correct!"
        else:
            st.session_state.last_feedback = f"❌ Incorrect! The correct answer was {correct_answer}"
    except ValueError:
        # If we couldn't convert to float, treat it as incorrect
        st.session_state.last_feedback = f"❌ Incorrect format. The correct answer was {correct_answer}"

    # Generate the next question
    st.session_state.current_question = generate_question(
        st.session_state.category,
        st.session_state.subcategory
    )

    # Clear the input box
    st.session_state.drill_input = ""

    # Force a rerun to refresh the question and time
    st.rerun()


def end_drill():
    """
    Ends the drill session and shows the final results.
    Resets the 'drill_in_progress' flag so user can start a new drill if desired.
    """
    st.session_state.drill_in_progress = False
    st.success("Time is up!")
    st.write(f"**Total Attempts:** {st.session_state.attempts}")
    st.write(f"**Correct Answers:** {st.session_state.score}")

    if st.session_state.attempts > 0:
        accuracy = (st.session_state.score / st.session_state.attempts) * 100
        st.write(f"**Accuracy:** {accuracy:.1f}%")
    else:
        st.write("No attempts recorded.")

    st.session_state.last_feedback = ""
    st.session_state.drill_input = ""


def generate_question(category, subcategory):
    """
    Returns a tuple (question_text, correct_answer).
    If subcategory is "All Basic Math" or "All Real-World Math", pick randomly
    from the relevant subcategories. Otherwise, pick the specified subcategory.
    """
    if category == "Basic Math":
        # Potential subcategories
        subs = ["Addition", "Subtraction", "Multiplication", "Division", "Percentages"]
        if subcategory == "All Basic Math":
            chosen_sub = random.choice(subs)
        else:
            chosen_sub = subcategory
        return generate_basic_math(chosen_sub)
    else:
        # Real-World Math
        subs = [
            "Interest Rates",
            "Growth Rates",
            "CAGR",
            "IRR",
            "Payback Period",
            "Break Even",
            "Profit Margins",
            "EBITDA"
        ]
        if subcategory == "All Real-World Math":
            chosen_sub = random.choice(subs)
        else:
            chosen_sub = subcategory
        return generate_real_world_math(chosen_sub)


def generate_basic_math(sub):
    """
    Generates a random basic math question and its answer.
    """
    if sub == "Addition":
        a, b = random.randint(1, 100), random.randint(1, 100)
        return (f"{a} + {b}", a + b)
    elif sub == "Subtraction":
        a, b = random.randint(1, 100), random.randint(1, 100)
        if b > a:  # ensure non-negative
            a, b = b, a
        return (f"{a} - {b}", a - b)
    elif sub == "Multiplication":
        a, b = random.randint(1, 12), random.randint(1, 12)
        return (f"{a} * {b}", a * b)
    elif sub == "Division":
        # Ensure integer division
        divisor = random.randint(1, 12)
        quotient = random.randint(1, 12)
        dividend = divisor * quotient
        return (f"{dividend} / {divisor}", quotient)
    elif sub == "Percentages":
        percent = random.choice([10, 15, 20, 25, 30, 40, 50])
        base = random.randint(50, 300)
        return (f"What is {percent}% of {base}?", (percent/100)*base)
    else:
        # Default fallback
        return ("Error: Unknown Basic Math Subcategory", 0)


def generate_real_world_math(sub):
    """
    Generates a random real-world math question and its answer.
    These are simplified examples, but can be expanded with more realism.
    """
    if sub == "Interest Rates":
        # E.g. "What is the interest earned on principal P at r% for T years?"
        P = random.randint(1000, 5000)
        r = random.randint(1, 10)  # interest rate in %
        T = random.randint(1, 5)
        question = f"Simple interest on ${P} at {r}% for {T} years?"
        answer = (P * r * T) / 100
        return (question, answer)

    elif sub == "Growth Rates":
        # "Value grows from A to B in T years. What is the overall growth rate (in %)?"
        A = random.randint(50, 500)
        B = A + random.randint(1, 200)
        T = random.randint(1, 5)
        growth = ((B - A) / A) * 100  # total growth % (not annualized)
        question = f"Value grows from {A} to {B} in {T} years. Total growth rate (%)?"
        return (question, growth)

    elif sub == "CAGR":
        # "Initial A, final B, T years, what's the CAGR?"
        A = random.randint(100, 1000)
        B = A + random.randint(1, 2000)
        T = random.randint(1, 5)
        # CAGR formula = (B/A)^(1/T) - 1
        cagr = ((B/A) ** (1/T) - 1) * 100
        question = f"Initial {A}, final {B}, over {T} years. CAGR (%)?"
        return (question, cagr)

    elif sub == "IRR":
        # Very simplified example with 2 cash flows only
        # "Invest X now, get Y after T years, what's the IRR?"
        X = random.randint(1000, 5000)
        T = random.randint(1, 5)
        Y = X + random.randint(1, 5000)
        # IRR is the r that satisfies: -X + (Y)/(1+r)^T = 0
        # We'll do a rough approximation for demonstration
        irr_approx = ((Y/X) ** (1/T) - 1) * 100
        question = f"Invest {X} now, receive {Y} in {T} years. Approx IRR (%)?"
        return (question, irr_approx)

    elif sub == "Payback Period":
        # "Cost C, yearly return R, how many years to break even?"
        C = random.randint(1000, 5000)
        R = random.randint(100, 1000)
        payback = round(C / R, 2)
        question = f"Project costs {C}, returns {R} per year. Payback period (years)?"
        return (question, payback)

    elif sub == "Break Even":
        # "Fixed cost F, variable cost v, price p, how many units to break even?"
        F = random.randint(500, 2000)
        v = random.randint(5, 20)
        p = v + random.randint(1, 15)
        be_units = round(F / (p - v), 2)
        question = f"Fixed cost={F}, var cost={v}, price={p}. Break-even units?"
        return (question, be_units)

    elif sub == "Profit Margins":
        # "Revenue R, Cost C, what's the profit margin in %?"
        R = random.randint(1000, 5000)
        C = random.randint(500, R)  # ensure cost <= revenue
        profit = R - C
        margin = (profit / R) * 100
        question = f"Revenue={R}, Cost={C}. Profit margin (%)?"
        return (question, margin)

    elif sub == "EBITDA":
        # "Net Income N, interest i, taxes t, depreciation d, amortization a -> EBITDA?"
        N = random.randint(100, 1000)
        i = random.randint(10, 200)
        t = random.randint(10, 200)
        d = random.randint(10, 200)
        a = random.randint(0, 200)
        ebitda = N + i + t + d + a
        question = f"NetIncome={N}, Interest={i}, Taxes={t}, Depr={d}, Amort={a}. EBITDA?"
        return (question, ebitda)

    else:
        # Default fallback
        return ("Error: Unknown Real-World Math Subcategory", 0)
