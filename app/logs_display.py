
import streamlit as st

def render_logs_view(log_file="app.log"):
    try:
        with open(log_file, "r") as f:
            logs = f.readlines()[-50:]
        st.sidebar.markdown("### Application Logs")
        with st.expander("View Logs", expanded=False):
            for log in logs:
                st.text(log.strip())
    except FileNotFoundError:
        st.sidebar.error("Log file not found.")
