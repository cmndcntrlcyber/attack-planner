import streamlit as st
from mitreattack import *
from pwn import *  # pwntools for payload generation
from attackcti import attack_client

import pandas as pd
import numpy as np
import json

import altair as alt
alt.renderers.enable('default')

import itertools

import logging
logging.getLogger('taxii2client').setLevel(logging.CRITICAL)

lift = attack_client()

# Function to fetch techniques associated with a threat actor
def fetch_techniques_for_actor(actor_name):
    """
    Fetch techniques associated with a given threat actor.
    """
    try:
        # Retrieve and serialize group data
        groups = lift.get_groups()
        groups_list = [json.loads(group.serialize()) for group in groups]

        # Normalize JSON into a DataFrame (for debugging and exploration)
        df = pd.json_normalize(groups_list)

        # Find the specified actor
        for group in groups_list:
            if actor_name.lower() in group.get('name', '').lower():
                return group.get('techniques', [])
        return []
    except Exception as e:
        print(f"Error fetching techniques: {e}")
        return []


# Function to validate and filter techniques
def validate_techniques(input_techniques, actor_techniques):
    valid_techniques = [t for t in input_techniques if t in actor_techniques]
    invalid_techniques = set(input_techniques) - set(valid_techniques)
    return valid_techniques, invalid_techniques

# Function to generate payloads for techniques
def generate_payloads(techniques):
    payloads = {}
    for technique in techniques:
        try:
            # Example payload generation based on technique
            if "T1059" in technique:  # Scripting
                payloads[technique] = asm(shellcraft.sh())  # Generate a shell payload
            elif "T1203" in technique:  # Exploitation for Client Execution
                payloads[technique] = cyclic(100)  # Generate a cyclic pattern
            else:
                payloads[technique] = f"Payload for {technique} is not implemented."
        except Exception as e:
            payloads[technique] = f"Error generating payload: {str(e)}"
    return payloads

# Streamlit App
def main():
    st.title("Threat Actor Payload Generator")

    # Input fields
    actor_name = st.text_input("Enter Threat Actor Name:")
    techniques_input = st.text_area("Enter Techniques (comma-separated):")

    # Button to fetch and generate payloads
    if st.button("Generate Payloads"):
        if not actor_name or not techniques_input:
            st.error("Please provide both a threat actor name and techniques.")
            return

        # Parse input techniques
        input_techniques = [t.strip() for t in techniques_input.split(',')]

        # Fetch techniques for actor
        with st.spinner("Fetching techniques for the threat actor..."):
            actor_techniques = fetch_techniques_for_actor(actor_name)
        if not actor_techniques:
            st.error(f"No techniques found for the threat actor: {actor_name}")
            return

        # Validate techniques
        valid_techniques, invalid_techniques = validate_techniques(input_techniques, actor_techniques)

        if invalid_techniques:
            st.warning(f"Invalid techniques ignored: {', '.join(invalid_techniques)}")

        # Generate payloads
        with st.spinner("Generating payloads..."):
            payloads = generate_payloads(valid_techniques)

        # Display payloads with download buttons
        st.success("Payloads generated successfully!")
        for technique, payload in payloads.items():
            st.subheader(f"Technique: {technique}")
            st.code(payload, language="bash")

            # Convert payload to bytes for download
            payload_bytes = payload.encode('utf-8')
            st.download_button(
                label=f"Download Payload for {technique}",
                data=payload_bytes,
                file_name=f"{technique}_payload.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
