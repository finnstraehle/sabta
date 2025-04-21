import streamlit as st
import random

st.title("Mental Math Drills")

def generate_question():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '/':
        num1 = num1 * num2  # Ensure division results in an integer
    question = f"{num1} {operation} {num2}"
    return question, eval(question)

if 'question' not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_question()

st.write("Solve the following problem:")
st.write(st.session_state.question)

user_answer = st.text_input("Your answer:")

if st.button("Submit"):
    if user_answer:
        if float(user_answer) == st.session_state.answer:
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct answer is {st.session_state.answer}")
        st.session_state.question, st.session_state.answer = generate_question()
    else:
        st.warning("Please enter an answer.")
