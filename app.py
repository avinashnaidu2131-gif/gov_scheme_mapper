import streamlit as st
import re
from model import find_eligible_schemes
from utils.helpers import load_schemes

st.set_page_config(page_title="Tamil Nadu Scheme Mapper", layout="centered")

st.title("AI Platform to Map Tamil Nadu Govt Schemes")

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
    ["Farmer", "Student", "Unemployed", "Private Job", "Government Employee"]
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female", "Other"]
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
        age, income, occupation, land, category, gender, schemes
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

    age_match = re.search(r'(\d{1,2})\s*year', text)
    age = int(age_match.group(1)) if age_match else 30

    income_match = re.search(r'(\d+)\s*lakh', text)
    if income_match:
        income = int(income_match.group(1)) * 100000
    else:
        income_number = re.search(r'(\d{5,7})', text)
        income = int(income_number.group(1)) if income_number else 200000

    if "farmer" in text:
        occupation = "Farmer"
    elif "student" in text:
        occupation = "Student"
    elif "unemployed" in text:
        occupation = "Unemployed"
    elif "government" in text:
        occupation = "Government Employee"
    else:
        occupation = "Private Job"

    if "female" in text or "woman" in text:
        gender = "Female"
    elif "male" in text:
        gender = "Male"
    else:
        gender = "Other"

    if "no land" in text:
        land = "No"
    elif "land" in text:
        land = "Yes"
    else:
        land = "No"

    if "sc" in text:
        category = "SC"
    elif "st" in text:
        category = "ST"
    elif "obc" in text:
        category = "OBC"
    else:
        category = "General"

    return age, income, occupation, land, category, gender


if st.button("Ask Chatbot"):

    age, income, occupation, land, category, gender = extract_details(user_input)

    results = find_eligible_schemes(
        age, income, occupation, land, category, gender, schemes
    )

    st.subheader("Eligible Schemes")

    if results:
        for name in results:
            st.success(f"✅ {name}")
    else:
        st.warning("No schemes eligible based on chatbot input.")