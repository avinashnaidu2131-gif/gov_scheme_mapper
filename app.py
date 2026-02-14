import streamlit as st
import re
from model import find_eligible_schemes
from utils.helpers import load_schemes

# Page config
st.set_page_config(page_title="Tamil Nadu Scheme Mapper", layout="centered")

st.title("AI Platform to Map Tamil Nadu Govt Schemes")

# Load scheme dataset
schemes = load_schemes()

# ===============================
# MANUAL ELIGIBILITY SECTION
# ===============================
st.header("Manual Eligibility Check")

age = st.slider("Age", 18, 80)

income = st.number_input(
    "Annual Income (₹)",
    min_value=0,
    step=1000
)

occupation = st.selectbox(
    "Occupation",
    ["Farmer", "Student", "Unemployed", "Private Job"]
)

land = st.selectbox(
    "Own Agricultural Land?",
    ["Yes", "No"]
)

category = st.selectbox(
    "Category",
    ["General", "OBC", "SC", "ST"]
)

if st.button("Find Eligible Schemes"):

    results = find_eligible_schemes(
        age, income, occupation, land, category, schemes
    )

    st.subheader("Eligible Schemes")

    if results:
        for name in results:
            st.success(f"✅ {name}")
    else:
        st.warning("No schemes eligible based on provided details.")

# ===============================
# CHATBOT SECTION
# ===============================
st.divider()
st.header("AI Scheme Assistant (Chatbot)")

user_input = st.text_area(
    "Describe your situation in simple English:"
)

def extract_details(text):

    text = text.lower()

    # Age extraction
    age_match = re.search(r'(\d{1,2})\s*year', text)
    age = int(age_match.group(1)) if age_match else 30

    # Income extraction
    income_match = re.search(r'(\d+)\s*lakh', text)
    if income_match:
        income = int(income_match.group(1)) * 100000
    else:
        income_number = re.search(r'(\d{5,7})', text)
        income = int(income_number.group(1)) if income_number else 200000

    # Occupation detection
    if "farmer" in text:
        occupation = "Farmer"
    elif "student" in text:
        occupation = "Student"
    elif "unemployed" in text:
        occupation = "Unemployed"
    else:
        occupation = "Private Job"

    # Land detection
    if "no land" in text:
        land = "No"
    elif "land" in text:
        land = "Yes"
    else:
        land = "No"

    # Category detection
    if "sc" in text:
        category = "SC"
    elif "st" in text:
        category = "ST"
    elif "obc" in text:
        category = "OBC"
    else:
        category = "General"

    return age, income, occupation, land, category


if st.button("Ask Chatbot"):

    age, income, occupation, land, category = extract_details(user_input)

    st.write("Detected Details:")
    st.write(f"Age: {age}")
    st.write(f"Income: ₹{income}")
    st.write(f"Occupation: {occupation}")
    st.write(f"Land: {land}")
    st.write(f"Category: {category}")

    results = find_eligible_schemes(
        age, income, occupation, land, category, schemes
    )

    st.subheader("Eligible Schemes")

    if results:
        for name in results:
            st.success(f"✅ {name}")
    else:
        st.warning("No schemes eligible based on chatbot input.")