import base64
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import os

st.set_page_config(page_title="Case Interview Practice Platform", layout="wide")
st.logo("data/sabta_logo.png", size="large")

# Title and welcome message
logo_path = os.path.join(os.path.dirname(__file__), "data", "sabta_logo.png")
if os.path.isfile(logo_path):
    # Encode logo for inline HTML
    logo_bytes = open(logo_path, "rb").read()
    logo_b64 = base64.b64encode(logo_bytes).decode()
    html_header = f"""
    <div style="text-align:center; margin-bottom:30px;">
      <img src="data:image/png;base64,{logo_b64}" width="300" style="margin-bottom:0px;" />
      <h1 font-size:2rem;">Interview Prep Platform & AI-Chat</h1>
    </div>
    """
    st.markdown(html_header, unsafe_allow_html=True)
else:
    st.warning("Logo 'mindra_logo.png' nicht gefunden.")

st.divider()
st.write(
    "This application helps **students prepare for case interviews** through comprehensive guides and interactive practice. "
    "Navigate using the pages in the sidebar: **Case Prep** for frameworks and tips, **Drills** for timed practice, and **Sparring** for a rapid Q&A simulation. "
    "Use this platform to improve your structuring, math, reasoning, and communication skills in a case interview setting."
)

# Example of a video
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
