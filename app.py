import streamlit as st
import pandas as pd
from model import find_eligible_schemes
from utils.helpers import load_schemes

st.set_page_config(page_title="TN Scheme Mapper", layout="wide")

st.title("Tamil Nadu Government Scheme Mapper")

schemes = load_schemes()

st.sidebar.header("Citizen Details")

age = st.sidebar.slider("Age", 18, 80)
income = st.sidebar.number_input("Annual Income (₹)", min_value=0)
occupation = st.sidebar.selectbox(
    "Occupation",
    ["Farmer","Student","Unemployed","Private Job","Government Employee"]
)
gender = st.sidebar.selectbox("Gender", ["Male","Female","Other"])
land = st.sidebar.selectbox("Own Agricultural Land?", ["Yes","No"])
category = st.sidebar.selectbox("Category", ["General","OBC","SC","ST"])
district = st.sidebar.selectbox(
    "District",
    ["Chennai","Coimbatore","Madurai","Salem","Tirunelveli"]
)

if st.sidebar.button("Check Eligibility"):

    results = find_eligible_schemes(
        age, income, occupation, land, category, gender, district, schemes
    )

    st.header("Eligible Schemes")

    if results:
        df = pd.DataFrame(results, columns=["Scheme","Category"])
        st.dataframe(df)

        # Dashboard
        st.header("Analytics Dashboard")

        st.metric("Total Eligible Schemes", len(df))

        category_count = df["Category"].value_counts()
        st.bar_chart(category_count)

    else:
        st.warning("No schemes eligible.")