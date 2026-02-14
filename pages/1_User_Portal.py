import streamlit as st
import pandas as pd
from model import find_eligible_schemes
from utils.helpers import load_schemes

st.title("Citizen Eligibility Portal")

schemes = load_schemes()

st.sidebar.header("Citizen Details")

age = st.sidebar.slider("Age", 18, 80)
income = st.sidebar.number_input("Annual Income (₹)", min_value=0)

occupation = st.sidebar.selectbox(
    "Occupation",
    ["Farmer","Student","Unemployed","Private Job","Government Employee","Fisherman","Salt Pan Worker"]
)

gender = st.sidebar.selectbox("Gender", ["Male","Female","Other"])

land = st.sidebar.selectbox("Own Agricultural Land?", ["Yes","No"])

category = st.sidebar.selectbox("Category", ["General","OBC","SC","ST"])

district = st.sidebar.selectbox(
    "District",
    [
        "Ariyalur","Chengalpattu","Chennai","Coimbatore","Cuddalore",
        "Dharmapuri","Dindigul","Erode","Kallakurichi","Kanchipuram",
        "Kanniyakumari","Karur","Krishnagiri","Madurai","Mayiladuthurai",
        "Nagapattinam","Namakkal","Nilgiris","Perambalur","Pudukkottai",
        "Ramanathapuram","Ranipet","Salem","Sivaganga","Tenkasi",
        "Thanjavur","Theni","Thiruvallur","Thiruvarur","Thoothukudi",
        "Tiruchirappalli","Tirunelveli","Tirupathur","Tiruppur",
        "Tiruvannamalai","Vellore","Viluppuram","Virudhunagar"
    ]
)

registration_status = st.sidebar.selectbox(
    "Registered in Welfare Board?",
    ["Yes","No"]
)

if st.sidebar.button("Check Eligibility"):

    results = find_eligible_schemes(
        age,
        income,
        occupation,
        land,
        category,
        gender,
        district,
        registration_status,
        schemes
    )

    st.header("Eligible Schemes")

    if results:
        df = pd.DataFrame(results, columns=["Scheme","Category"])
        st.dataframe(df)

        st.metric("Total Eligible Schemes", len(df))
        st.bar_chart(df["Category"].value_counts())
    else:
        st.warning("No schemes eligible.")