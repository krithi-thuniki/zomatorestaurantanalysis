# sidebar.py
import streamlit as st

def show_sidebar():
    role = st.session_state.get("role", None)
    st.sidebar.title("Navigation")

    if role == "admin":
        page = st.sidebar.radio("Go to", ["Data Upload", "Machine Learning Predictions"])
    elif role == "user":
        page = st.sidebar.radio("Go to", ["EDA Dashboard", "Visualization Dashboard"])
    else:
        page = None
    return page
