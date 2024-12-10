
import streamlit as st

def reset_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
