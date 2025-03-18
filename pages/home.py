import streamlit as st

def home_page():
    """
    A simple Home page. You can expand this with welcome text,
    user instructions, or general announcements.
    """
    st.title("Home Page")
    st.write("Welcome to the Case Interview Prep Platform!")
    st.write("""
    Use the sidebar to navigate:
    - **Case Prep** for case interview resources.
    - **Drills** for quick math and real-world problem exercises.
    - **Sparring** for mock interviews or practice sessions.
    """)
