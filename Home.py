import streamlit as st
import pandas as pd
import altair as alt

# Set page config for the main page (Home)
st.set_page_config(page_title="Home", layout="wide")

# Title and welcome message
st.title("Case Interview Practice Platform")
st.subheader("Welcome!")
st.write(
    "This application helps **students prepare for case interviews** through comprehensive guides and interactive practice. "
    "Navigate using the pages in the sidebar: **Case Prep** for frameworks and tips, **Drills** for timed practice, and **Sparring** for a rapid Q&A simulation. "
    "Use this platform to improve your structuring, math, reasoning, and communication skills in a case interview setting."
)
