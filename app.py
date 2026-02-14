import streamlit as st
import pandas as pd
from model import find_eligible_schemes
from utils.helpers import load_schemes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TN Revenue Scheme Mapper", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-title {
    font-size:32px;
    font-weight:700;
    color:#0E4C92;
}
.section-title {
    font-size:20px;
    font-weight:600;
    margin-top:20px;
}
.card {
    padding:20px;
    border-radius:12px;
    background-color:#f5f9ff;
    margin-bottom:15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.footer {
    text-align:center;
    font-size:14px;
    color:gray;
    margin-top:50px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Tamil Nadu Revenue Integrated Scheme Mapper</div>', unsafe_allow_html=True)

schemes = load_schemes()

# ---------------- SIDEBAR ----------------
st.sidebar.header("Citizen Information")

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

st.sidebar.markdown("---")
st.sidebar.subheader("Revenue Verification")

income_verified = st.sidebar.selectbox(
    "Income Certificate Verified?",
    ["Yes","No"]
)

patta_number = st.sidebar.text_input("Patta Number")
caste_certificate = st.sidebar.text_input("Caste Certificate Number")
family_card_number = st.sidebar.text_input("Family Card Number")

# ---------------- BUTTON ----------------
if st.sidebar.button("Check Eligibility"):

    results = find_eligible_schemes(
        age, income, occupation, land, category, gender,
        district, schemes, registration_status,
        income_verified, patta_number,
        caste_certificate, family_card_number
    )

    st.markdown('<div class="section-title">Eligible Schemes</div>', unsafe_allow_html=True)

    if results:

        df = pd.DataFrame(results, columns=["Scheme","Category"])

        # -------- CARD STYLE OUTPUT --------
        for index, row in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <h4>{row['Scheme']}</h4>
                <p><b>Category:</b> {row['Category']}</p>
            </div>
            """, unsafe_allow_html=True)

        # -------- DASHBOARD --------
        st.markdown('<div class="section-title">Analytics Dashboard</div>', unsafe_allow_html=True)

        st.metric("Total Eligible Schemes", len(df))
        st.bar_chart(df["Category"].value_counts())

        # -------- PDF --------
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
        st.warning("No schemes eligible based on provided revenue verification.")

st.markdown('<div class="footer">© 2026 Tamil Nadu Revenue Department Hackathon Project</div>', unsafe_allow_html=True)