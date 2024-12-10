
import streamlit as st
import pandas as pd

def filter_results(results_df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    if not search_term.strip():
        return results_df

    filtered_df = results_df[
        results_df["Technique"].str.contains(search_term, case=False, na=False)
        | results_df["Description"].str.contains(search_term, case=False, na=False)
    ]
    return filtered_df

def render_search_bar():
    search_term = st.text_input("Search Techniques or Descriptions")
    return search_term
