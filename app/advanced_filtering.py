
import streamlit as st
import pandas as pd

def multi_select_filter(results_df: pd.DataFrame, categories: list):
    if not categories:
        return results_df
    filtered_df = results_df[results_df["Technique"].isin(categories)]
    return filtered_df

def render_advanced_filters(results_df: pd.DataFrame):
    techniques = results_df["Technique"].unique().tolist()
    selected_categories = st.multiselect(
        "Filter by Technique Categories", techniques, default=st.session_state.selected_categories
    )
    st.session_state.selected_categories = selected_categories
    return selected_categories
