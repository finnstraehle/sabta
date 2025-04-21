import streamlit as st
import time


st.set_page_config(page_title="Case Interview Prep", page_icon=":briefcase:", layout="wide")

st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: auto;
        }
        .title {
            font-size: 2.5em;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 10px;
        }
        .subheader {
            font-size: 1.5em;
            color: #555;
            text-align: center;
            margin-bottom: 20px;
        }
        .features, .get-started {
            margin-top: 30px;
        }
        .features ul, .get-started ul {
            list-style-type: none;
            padding: 0;
        }
        .features li, .get-started li {
            background: #fff;
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .features li::before, .get-started li::before {
            content: "✔";
            color: #4CAF50;
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)
st.markdown('<div class="title">Welcome to Case Interview Prep</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Your ultimate resource for mastering case interviews</div>', unsafe_allow_html=True)

st.write("""
We provide a comprehensive set of tools and resources to help you prepare for your case interviews.
Whether you are a beginner or an experienced candidate, our platform offers valuable insights and practice materials to help you succeed.
""")

st.markdown('<div class="features">', unsafe_allow_html=True)
st.write("### Features:")
st.markdown("""
<ul>
    <li>Interactive case studies</li>
    <li>Expert tips and strategies</li>
    <li>Practice questions and answers</li>
    <li>Community forums and discussions</li>
    <li>Personalized feedback and coaching</li>
</ul>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="get-started">', unsafe_allow_html=True)
st.write("### Get Started:")
st.markdown("""
<ul>
    <li>Sign up today and start your journey towards acing your case interviews!</li>
</ul>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
