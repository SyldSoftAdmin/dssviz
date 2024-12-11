import streamlit as st

st.title("DSS Visualizer")
st.write("Welcome to the **DSS Visualizer** App!")

# Add a simple progress bar
progress = st.slider("Task Completion", 0, 100, 50)
st.progress(progress)

# Example button
if st.button("Click Me"):
    st.write("Button clicked!")