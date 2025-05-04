import streamlit as st
import pandas as pd
import numpy as np


# Page Title
st.title("Learning and Experimentation Page")

# Introduction
st.write("""
Welcome to your learning and experimentation page!
Here, you can explore various Streamlit components and see what you can build.
""")

# Text Input
name = st.text_input("What's your name?", "")
if name:
    st.write(f"Hello, {name}! 👋")

# Slider
age = st.slider("How old are you?", 0, 100, 25)
st.write(f"You are {age} years old.")

# Checkbox
if st.checkbox("Show a secret message"):
    st.write("🎉 You found the secret message!")

# Selectbox
favorite_language = st.selectbox(
    "What's your favorite programming language?",
    ["Python", "JavaScript", "C++", "Java", "Other"]
)
st.write(f"Your favorite programming language is {favorite_language}.")

# Button
if st.button("Click me!"):
    st.write("You clicked the button! 🚀")

# File Uploader
uploaded_file = st.file_uploader("Upload a file")
if uploaded_file:
    st.write(f"Uploaded file: {uploaded_file.name}")

# Data Visualization Example

st.write("Here's a random financial data visualization:")
# Generate random financial data
dates = pd.date_range(start="2023-01-01", periods=30)
data = pd.DataFrame({
    "Date": dates,
    "Stock Price": np.random.uniform(100, 200, size=30),
    "Volume": np.random.randint(1000, 5000, size=30)
}).set_index("Date")

# Select chart type
chart_type = st.selectbox("Select chart type", ["Line Chart", "Bar Chart"])

if chart_type == "Line Chart":
    st.line_chart(data[["Stock Price"]])
elif chart_type == "Bar Chart":
    st.bar_chart(data[["Volume"]])

# Footer
st.write("Happy coding! 🎉")
