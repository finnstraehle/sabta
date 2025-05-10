import base64
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import os

st.set_page_config(page_title="SABTA – Interview Practice Platform", layout="wide")
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

# Problem statement and use case – Outstanding Implementation (3/4)
with st.container():
    st.markdown(
        """
        <div style="padding: 20px; border: 2px solid #4A90E2; border-radius: 10px; background-color: #F5F9FF;">
            <h2 style="color: #4A90E2; text-align: center; margin-bottom: 15px;">Clearly Defined Problem & Use Case</h2>
            <p style="font-size: 15px; line-height: 1.6; margin: 8px 0;">
                As students navigating the challenging world of consulting and finance, our team faced a common yet daunting problem: preparation for case interviews is overwhelmingly fragmented. With resources scattered across countless websites, PDF guides, forums, and books, preparation often felt disjointed, chaotic, and inefficient.
            </p>
            <p style="font-size: 15px; line-height: 1.6; margin: 8px 0;">
                We repeatedly experienced the frustration of losing crucial preparation time simply switching between various sources and tools—this wasn’t just inconvenient; it significantly impacted our confidence and readiness. Interviews are stressful enough, and the lack of a cohesive, integrated preparation platform magnified that anxiety.
            </p>
            <p style="font-size: 15px; line-height: 1.6; margin: 8px 0;">
                After collectively attending over 200 interviews at top-tier consulting and finance firms, we realized a critical gap existed in accessible, integrated, and genuinely effective interview preparation. Out of necessity and personal ambition, we decided to build the solution we wished we had from day one.
            </p>
            <h3 style="color: #4A90E2; margin-top: 20px;">Our Comprehensive Solution</h3>
            <p style="font-size: 15px; line-height: 1.6; margin: 8px 0;">
                This platform unites every essential element into one intuitive interface:
                guided frameworks, timed math drills, real data analytics, and interactive
                sparring—powered by AI.
            </p>
            <p style="font-size: 15px; line-height: 1.6; margin: 8px 0;">
                Students can seamlessly flow from learning the core concepts to practicing
                under pressure, reviewing analytics on their performance, and sharpening
                their communication skills with a simulated partner.
            </p>
            <h3 style="color: #4A90E2; margin-top: 20px;">Key Features at a Glance</h3>
            <ul style="font-size: 15px; line-height: 1.6;">
                <li><strong>Case Prep Guides:</strong> Structured frameworks, interactive hints, and real-world examples.</li>
                <li><strong>Math Drills:</strong> Timed questions across four difficulty levels to build speed and accuracy.</li>
                <li><strong>Finance Analytics:</strong> Live market data, chart tools, and scenario simulations.</li>
                <li><strong>Interview Sparring:</strong> Peer-modeled Q&A rounds for live feedback and scoring.</li>
                <li><strong>AI-Powered Sparring:</strong> A smart partner that adapts questions to your skill level in real time.</li>
            </ul>
            <h3 style="color: #4A90E2; margin-top: 20px;">Why It Matters</h3>
            <p style="font-size: 15px; line-height: 1.6; margin: 8px 0;">
                By centralizing all interview prep tools, students regain control and clarity—
                fostering confidence, reducing anxiety, and dramatically improving outcomes.
            </p>
            <h3 style="color: #4A90E2; margin-top: 20px;">About Our Team</h3>
            <p style="font-size: 15px; line-height: 1.6; margin: 8px 0;">
                Built by four friends who collectively completed 200+ interviews at top firms,
                we’ve distilled years of firsthand experience into this platform. Every line of
                code, chart, and question reflects our own journey and rigorous research.
            </p>
            <p style="font-size: 15px; line-height: 1.6; margin: 8px 0;">
                Our goal: empower every candidate to feel prepared, supported, and ready to
                excel—no matter how complex the case or tight the schedule.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
