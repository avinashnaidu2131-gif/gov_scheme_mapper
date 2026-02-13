import streamlit as st
from model import find_eligible_schemes
from utils.helpers import load_schemes

st.set_page_config(page_title="Scheme Mapper")

st.title("AI Platform to Map Govt Schemes to Beneficiaries")

# Load scheme dataset
schemes = load_schemes()

st.header("Enter Citizen Details")

age = st.slider("Age", 18, 80)
income = st.number_input("Annual Income (₹)", min_value=0)
occupation = st.selectbox(
    "Occupation",
    ["Farmer","Student","Unemployed","Private Job"]
)
land = st.selectbox("Own Agricultural Land?", ["Yes","No"])
category = st.selectbox(
    "Category",
    ["General","OBC","SC","ST"]
)

# Run model
if st.button("Find Eligible Schemes"):
    results = find_eligible_schemes(
        age,
        income,
        occupation,
        land,
        category,
        schemes
    )

    if results:
        st.success("Eligible Schemes")
        for r in results:
            st.write(f"✅ {r}")
    else:
        st.warning("No schemes matched")