
# Main Streamlit App
import streamlit as st
from data_fetcher import fetch_techniques
from payload_generator import process_techniques
from app_ui import render_header, display_payload_table, show_pie_chart, download_payloads
from filtering import filter_results, render_search_bar
from advanced_filtering import render_advanced_filters, multi_select_filter
from persistent_state import initialize_session_state
from logger import setup_logger
from logs_display import render_logs_view
from reset_handler import reset_session_state

logger = setup_logger()
initialize_session_state()

render_header("Complete Threat Payload Generator")

st.sidebar.header("Configuration")
threat_actor = st.sidebar.text_input("Threat Actor Name", value=st.session_state.get("last_actor", ""))
techniques_input = st.sidebar.text_area("Techniques (comma-separated)", value=st.session_state.get("last_techniques", ""))

if st.sidebar.button("Reset App"):
    reset_session_state()
    st.experimental_rerun()

if st.sidebar.button("Generate Payloads"):
    if not threat_actor or not techniques_input:
        st.error("Please provide both a threat actor and techniques.")
        logger.error("Missing input: Threat actor or techniques not provided.")
    else:
        st.session_state.last_actor = threat_actor
        st.session_state.last_techniques = techniques_input
        st.info("Validating threat actor and techniques...")
        logger.info("Starting payload generation process.")
        try:
            input_techniques = [t.strip() for t in techniques_input.split(",")]
            all_techniques = fetch_techniques()
            payload_results = process_techniques(input_techniques, all_techniques)
            st.session_state.payload_results.extend(payload_results)
            logger.info("Payload generation completed successfully.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
            logger.error(f"Error during payload generation: {e}")

search_term = render_search_bar()
st.session_state.search_term = search_term

results_df = pd.DataFrame(st.session_state.payload_results)
filtered_results = filter_results(results_df, search_term)
selected_categories = render_advanced_filters(filtered_results)
final_results = multi_select_filter(filtered_results, selected_categories)

display_payload_table(final_results)
show_pie_chart(final_results)
download_payloads(final_results)

render_logs_view()
