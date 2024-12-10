
import streamlit as st

def initialize_session_state():
    if "payload_results" not in st.session_state:
        st.session_state.payload_results = []
    if "search_term" not in st.session_state:
        st.session_state.search_term = ""
    if "selected_categories" not in st.session_state:
        st.session_state.selected_categories = []
    if "log_messages" not in st.session_state:
        st.session_state.log_messages = []
