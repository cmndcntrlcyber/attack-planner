
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def render_header(title: str):
    st.title(title)

def display_payload_table(payload_results):
    st.subheader("Generated Payloads")
    results_df = pd.DataFrame(payload_results)
    st.dataframe(results_df)
    return results_df

def show_pie_chart(results_df):
    st.subheader("Payload Generation Summary")
    fig, ax = plt.subplots(figsize=(10, 5))
    results_df["Found"] = results_df["Description"] != "Not Found"
    found_data = results_df["Found"].value_counts()
    ax.pie(
        found_data, labels=["Found", "Not Found"], autopct="%1.1f%%", startangle=140
    )
    st.pyplot(fig)

def download_payloads(results_df):
    csv_data = results_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="payload_results.csv",
        mime="text/csv",
    )
