import streamlit as st
from utils.helpers import load_schemes

st.title("AI Scheme Assistant")

schemes = load_schemes()

question = st.text_input("Ask about schemes...")

if question:
    matched = []

    for scheme in schemes:
        if question.lower() in scheme["name"].lower():
            matched.append(scheme["name"])

    if matched:
        st.write("Matching Schemes:")
        for m in matched:
            st.write("•", m)
    else:
        st.write("No direct match found.")