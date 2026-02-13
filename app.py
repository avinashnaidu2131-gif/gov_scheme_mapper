import streamlit as st
from model import find_eligible_schemes
from utils.helpers import load_schemes

# Page settings
st.set_page_config(page_title="Gov Scheme Mapper", layout="centered")

st.title("AI Platform to Map Govt Schemes to Beneficiaries")

# Load schemes dataset
schemes = load_schemes()

st.header("Enter Citizen Details")

# -------- Input Fields --------
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

# -------- Button --------
if st.button("Find Eligible Schemes"):

    results = find_eligible_schemes(
        age,
        income,
        occupation,
        land,
        category,
        schemes
    )

    st.subheader("Eligibility Results")

    # -------- Display --------
    for name, status in results:

        if status == "Eligible":
            st.success(f"✅ {name} — Eligible")

        else:
            st.error(f"❌ {name} — Not Eligible")
