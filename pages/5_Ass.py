import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import random
import time


# Streamlit elements library
st.title("Streamlit Elements Library")
st.header("Headers and Subheaders")
st.subheader("This is a subheader")

st.text("This is a simple text.")
st.markdown("**Markdown** allows for *formatting*.")

st.write("Write can display various objects, like this dictionary:", {"key": "value"})

st.code("print('This is a code block')", language="python")

st.latex(r"a^2 + b^2 = c^2")

st.button("Click Me")

st.write("This is a container.")

if st.checkbox("Check me"):
    st.write("Checkbox is checked!")

option = st.radio("Choose an option:", ["Option 1", "Option 2", "Option 3"])
st.write(f"You selected: {option}")

dropdown = st.selectbox("Select an item:", ["Item 1", "Item 2", "Item 3"])
st.write(f"You selected: {dropdown}")

multi_select = st.multiselect("Select multiple items:", ["Item A", "Item B", "Item C"])
st.write(f"You selected: {multi_select}")

slider = st.slider("Slide me:", 0, 100, 50)
st.write(f"Slider value: {slider}")

number_input = st.number_input("Enter a number:", min_value=0, max_value=100, value=50)
st.write(f"Number input: {number_input}")

text_input = st.text_input("Enter some text:")
st.write(f"Text input: {text_input}")

text_area = st.text_area("Enter a longer text:")
st.write(f"Text area: {text_area}")

date_input = st.date_input("Pick a date:")
st.write(f"Date input: {date_input}")

time_input = st.time_input("Pick a time:")
st.write(f"Time input: {time_input}")

file_upload = st.file_uploader("Upload a file:")
if file_upload:
    st.write("File uploaded!")

color_picker = st.color_picker("Pick a color:")
st.write(f"Color picked: {color_picker}")

st.sidebar.title("Sidebar Elements")
st.sidebar.button("Sidebar Button")


st.sidebar.checkbox("Sidebar Checkbox")
st.sidebar.radio("Sidebar Radio", ["Option A", "Option B", "Option C"])
st.sidebar.selectbox("Sidebar Selectbox", ["Item X", "Item Y", "Item Z"])
st.sidebar.multiselect("Sidebar Multiselect", ["Item 1", "Item 2", "Item 3"])
st.sidebar.slider("Sidebar Slider", 0, 100, 50)
st.sidebar.number_input("Sidebar Number Input", min_value=0, max_value=100, value=50)
st.sidebar.text_input("Sidebar Text Input")
st.sidebar.text_area("Sidebar Text Area")

# Example of a simple Altair chart
data = pd.DataFrame({
    'x': range(10),
    'y': [random.randint(0, 100) for _ in range(10)]
})

chart = alt.Chart(data).mark_line().encode(
    x='x',
    y='y'
)

st.altair_chart(chart, use_container_width=True)

# Example of a DataFrame display
df = pd.DataFrame({
    'Column 1': [1, 2, 3, 4],
    'Column 2': ['A', 'B', 'C', 'D']
})

st.write("Here is a sample DataFrame:")
st.dataframe(df)

# Example of a progress bar
progress_bar = st.progress(0)
for i in range(100):
    progress_bar.progress(i + 1)

# Example of a success message
st.success("This is a success message!")

# Example of an error message
st.error("This is an error message!")

# Example of a warning message
st.warning("This is a warning message!")

# Example of an info message
st.info("This is an info message!")

# Example of a balloon animation
st.balloons()

# Example of a spinner
with st.spinner("Loading..."):
    time.sleep(2)
# Example of a map
st.map(pd.DataFrame({
    'lat': [37.7749, 34.0522],
    'lon': [-122.4194, -118.2437]
}))
# Example of a table
st.table(df)
# Example of a metric
st.metric(label="Temperature", value="72 °F", delta="1 °F")
# Example of a download button
st.download_button("Download CSV", df.to_csv(), "data.csv", "text/csv")
# Example of a markdown with HTML
st.markdown("<h1 style='color:blue;'>This is a header with HTML</h1>", unsafe_allow_html=True)
# Example of a video
st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
# Example of an audio
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
# Example of a progress bar with a custom message
progress_bar = st.progress(0, text="Loading...")
for i in range(100):
    progress_bar.progress(i + 1, text=f"Loading... {i + 1}%")
# Example of a custom HTML component
st.components.v1.html("<h1 style='color:red;'>This is a custom HTML component</h1>", height=100)
# Example of a custom CSS
st.markdown(
    """
    <style>
    .custom-css {
        color: green;
        font-size: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<p class="custom-css">This is a custom CSS styled text</p>', unsafe_allow_html=True)
# Example of a custom JavaScript
st.components.v1.html(
    """
    <script>
    alert("This is a custom JavaScript alert!");
    </script>
    """,
    height=0
)
# Example of a custom HTML component with JavaScript
st.components.v1.html(
    """
    <div>
        <h1>This is a custom HTML component with JavaScript</h1>
        <button onclick="alert('Button clicked!')">Click me!</button>
    </div>
    """,
    height=100
)
# Example of a custom HTML component with CSS
st.components.v1.html(
    """
    <style>
    .custom-html {
        color: purple;
        font-size: 30px;
    }
    </style>
    <div class="custom-html">
        <h1>This is a custom HTML component with CSS</h1>
    </div>
    """,
    height=100
)
# Example of a custom HTML component with CSS and JavaScript
st.components.v1.html(
    """
    <style>
    .custom-html-js {
        color: orange;
        font-size: 25px;
    }
    </style>
    <div class="custom-html-js">
        <h1>This is a custom HTML component with CSS and JavaScript</h1>
        <button onclick="alert('Button clicked!')">Click me!</button>
    </div>
    """,
    height=100
)
# Example of a custom HTML component with CSS and JavaScript and a form
st.components.v1.html(
    """
    <style>
    .custom-html-form {
        color: pink;
        font-size: 20px;
    }
    </style>
    <div class="custom-html-form">
        <h1>This is a custom HTML component with CSS and JavaScript and a form</h1>
        <form onsubmit="alert('Form submitted!'); return false;">
            <input type="text" placeholder="Enter something...">
            <button type="submit">Submit</button>
        </form>
    </div>
    """,
    height=100
)

# Example of a session state usage
if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment Counter"):
    st.session_state.counter += 1

st.write(f"Counter value: {st.session_state.counter}")

# Example of a Streamlit form
with st.form("my_form"):
    st.write("Inside the form")
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=0, max_value=120)
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(f"Hello {name}, you are {age} years old!")

# Example of a Streamlit expander
with st.expander("See explanation"):
    st.write("""
        This is an example of a Streamlit expander.
        You can use it to hide and show content dynamically.
    """)

# Example of a Streamlit tabs
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.write("This is Tab 1")
with tab2:
    st.write("This is Tab 2")
with tab3:
    st.write("This is Tab 3")
csv = df.to_csv(index=False).encode('utf-8')

# Example of a Streamlit file uploader with file processing
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded DataFrame:")
    st.dataframe(data)

# Example of a Streamlit chart with user input
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
chart_type = st.selectbox("Select chart type", ["Line", "Bar", "Area"])
if chart_type == "Line":
    st.line_chart(chart_data)
elif chart_type == "Bar":
    st.bar_chart(chart_data)
elif chart_type == "Area":
    st.area_chart(chart_data)

# Example of a Streamlit interactive map
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)
st.map(map_data)

# Example of a Streamlit session state with a counter
if "count" not in st.session_state:
    st.session_state.count = 0

increment = st.button("Increment")
if increment:
    st.session_state.count += 1

st.write(f"Current count: {st.session_state.count}")

# Example of Streamlit file download with user input
text_to_download = st.text_area("Enter text to download:")
if text_to_download:
    st.download_button(
        label="Download Text",
        data=text_to_download,
        file_name="text.txt",
        mime="text/plain"
    )

# Example of Streamlit image display
st.image("https://via.placeholder.com/150", caption="Sample Image")

# Example of Streamlit camera input
camera_input = st.camera_input("Take a picture")
if camera_input:
    st.image(camera_input)

# Example of Streamlit date range picker
date_range = st.date_input("Select a date range", [], help="Pick a start and end date", key="date_range", on_change=None)
if len(date_range) == 2:
    st.write(f"Start date: {date_range[0]}, End date: {date_range[1]}")

# Example of Streamlit file uploader with image preview
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image")

# Example of Streamlit toggle switch
toggle = st.toggle("Enable feature")
if toggle:
    st.write("Feature enabled!")
else:
    st.write("Feature disabled!")

# Example of Streamlit pagination
page = st.number_input("Page", min_value=1, max_value=10, step=1)
st.write(f"You are on page {page}")

# Example of Streamlit code editor
code = st.text_area("Write your code here:")
if code:
    st.code(code, language="python")
