import streamlit as st
import pandas as pd
from model import find_eligible_schemes
from utils.helpers import load_schemes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="TN Revenue Scheme Mapper", layout="wide")

st.title("Tamil Nadu Revenue Integrated Scheme Mapper")

schemes = load_schemes()

# ---------------- SIDEBAR ----------------
st.sidebar.header("Citizen Details")

age = st.sidebar.slider("Age", 18, 80)
income = st.sidebar.number_input("Annual Income (₹)", min_value=0)

occupation = st.sidebar.selectbox(
    "Occupation",
    ["Farmer","Student","Unemployed","Private Job",
     "Government Employee","Fisherman","Salt Pan Worker"]
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

# -------- Revenue Verification --------
st.sidebar.subheader("Revenue Verification")

income_verified = st.sidebar.selectbox(
    "Income Certificate Verified?",
    ["Yes","No"]
)

patta_number = st.sidebar.text_input("Patta Number (Land Record ID)")
caste_certificate = st.sidebar.text_input("Caste Certificate Number")
family_card_number = st.sidebar.text_input("Family Card Number")

# ---------------- CHECK ----------------
if st.sidebar.button("Check Eligibility"):

    results = find_eligible_schemes(
        age, income, occupation, land, category, gender, district,
        schemes, registration_status,
        income_verified, patta_number,
        caste_certificate, family_card_number
    )

    st.header("Eligible Schemes")

    if results:

        df = pd.DataFrame(results, columns=["Scheme","Category"])
        st.dataframe(df)

        st.header("Analytics Dashboard")
        st.metric("Total Eligible Schemes", len(df))
        st.bar_chart(df["Category"].value_counts())

        # PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("Eligible Schemes", styles["Heading1"]))
        elements.append(Spacer(1, 12))

        for scheme in df["Scheme"]:
            elements.append(Paragraph(scheme, styles["Normal"]))
            elements.append(Spacer(1, 6))

        doc.build(elements)
        buffer.seek(0)

        st.download_button(
            label="Download PDF Report",
            data=buffer,
            file_name="eligibility_report.pdf",
            mime="application/pdf"
        )

    else:
        st.warning("No schemes eligible.")