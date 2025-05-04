import streamlit as st
import pandas as pd
import altair as alt

# Set page config for the main page (Home)
st.set_page_config(page_title="Case Interview Prep App", layout="wide")

# Initialize session state for user stats if not already done.
# This will track total questions attempted and correct per drill category.
if 'stats' not in st.session_state:
    st.session_state.stats = {
        "Basic Math": {"attempted": 0, "correct": 0},
        "Real World Math": {"attempted": 0, "correct": 0},
        "Logical Reasoning": {"attempted": 0, "correct": 0},
        "Numerical Reasoning": {"attempted": 0, "correct": 0},
        "Chart Analysis": {"attempted": 0, "correct": 0},
        "Verbal Reasoning": {"attempted": 0, "correct": 0},
    }

# Title and welcome message
st.title("Case Interview Practice Platform")
st.subheader("Welcome!")
st.write(
    "This application helps **students prepare for case interviews** through comprehensive guides and interactive practice. "
    "Navigate using the pages in the sidebar: **Case Prep** for frameworks and tips, **Drills** for timed practice, and **Sparring** for a rapid Q&A simulation. "
    "Use this platform to improve your structuring, math, reasoning, and communication skills in a case interview setting."
)

# Optionally, include a banner image or graphic for visual appeal (using a placeholder image here).
# st.image("https://via.placeholder.com/800x200.png?text=Case+Interview+Prep", use_column_width=True)
