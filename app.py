import streamlit as st
import re
from model import find_eligible_schemes
from utils.helpers import load_schemes

st.set_page_config(page_title="Gov Scheme Mapper", layout="centered")

st.title("AI Platform to Map Govt Schemes to Beneficiaries")

schemes = load_schemes()

# =========================
# MANUAL FORM SECTION
# =========================
st.header("Manual Eligibility Check")

age = st.slider("Age", 18, 80)
income = st.number_input("Annual Income (₹)", min_value=0, step=1000)

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

    st.subheader("Eligibility Results")

    for name, status in results:
        if status == "Eligible":
            st.success(f"✅ {name} — Eligible")
        else:
            st.error(f"❌ {name} — Not Eligible")

# =========================
# CHATBOT SECTION
# =========================
st.header("AI Scheme Assistant (Chatbot)")

user_input = st.text_area(
    "Describe your situation in simple English:"
)

def extract_details(text):

    # Age
    age_match = re.search(r'(\d{1,2})\s*year', text.lower())
    age = int(age_match.group(1)) if age_match else 30

    # Income
    income_match = re.search(r'(\d+)\s*lakh', text.lower())
    if income_match:
        income = int(income_match.group(1)) * 100000
    else:
        income_number = re.search(r'(\d{5,7})', text)
        income = int(income_number.group(1)) if income_number else 200000

    # Occupation
    if "farmer" in text.lower():
        occupation = "Farmer"
    elif "student" in text.lower():
        occupation = "Student"
    elif "unemployed" in text.lower():
        occupation = "Unemployed"
    else:
        occupation = "Private Job"

    # Land
    if "land" in text.lower() and "no land" not in text.lower():
        land = "Yes"
    else:
        land = "No"

    # Category
    if "sc" in text.lower():
        category = "SC"
    elif "st" in text.lower():
        category = "ST"
    elif "obc" in text.lower():
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

    st.subheader("Chatbot Eligibility Results")

    for name, status in results:
        if status == "Eligible":
            st.success(f"✅ {name} — Eligible")
        else:
            st.error(f"❌ {name} — Not Eligible")