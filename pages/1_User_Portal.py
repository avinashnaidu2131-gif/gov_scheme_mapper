import streamlit as st
import pandas as pd
from model import find_eligible_schemes
from utils.helpers import load_schemes

if st.session_state.role != "Citizen":
    st.warning("Access Denied")
    st.stop()

st.title("Citizen Eligibility Portal")

schemes = load_schemes()

age = st.slider("Age", 18, 80)
income = st.number_input("Annual Income (₹)", min_value=0)

occupation = st.selectbox("Occupation",
    ["Farmer","Student","Unemployed","Private Job",
     "Government Employee","Fisherman","Salt Pan Worker"])

gender = st.selectbox("Gender", ["Male","Female","Other"])
land = st.selectbox("Own Agricultural Land?", ["Yes","No"])
category = st.selectbox("Category", ["General","OBC","SC","ST"])
district = st.text_input("District")

registration_status = st.selectbox("Registered in Welfare Board?", ["Yes","No"])
income_verified = st.selectbox("Income Certificate Verified?", ["Yes","No"])

patta_number = st.text_input("Patta Number")
caste_certificate = st.text_input("Caste Certificate Number")
family_card_number = st.text_input("Family Card Number")

if st.button("Check Eligibility"):

    results = find_eligible_schemes(
        age,
        income,
        occupation,
        land,
        category,
        gender,
        district,
        schemes,
        registration_status,
        income_verified,
        patta_number,
        caste_certificate,
        family_card_number
    )

    if results:
        df = pd.DataFrame(results, columns=["Scheme","Category"])
        st.dataframe(df)

        st.metric("Total Eligible Schemes", len(df))
        st.bar_chart(df["Category"].value_counts())
    else:
        st.warning("No eligible schemes found.")