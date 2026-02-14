import streamlit as st
import pandas as pd
from model import find_eligible_schemes
from utils.helpers import load_schemes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="TN Revenue Scheme Mapper", layout="wide")

# ---------------- SESSION STATE ----------------
if "results" not in st.session_state:
    st.session_state.results = None

if "language" not in st.session_state:
    st.session_state.language = "English"

# ---------------- LANGUAGE SWITCH ----------------
st.sidebar.title("Settings")
language = st.sidebar.selectbox("Language / மொழி", ["English", "Tamil"])
st.session_state.language = language

# ---------------- TEXT TRANSLATIONS ----------------
TEXT = {
    "English": {
        "title": "Tamil Nadu Revenue Integrated Scheme Mapper",
        "subtitle": "Digitally Mapping Verified Beneficiaries to Government Welfare Schemes",
        "citizen": "Citizen Details",
        "check": "Check Eligibility",
        "eligible": "Eligible Schemes",
        "search": "Search Scheme",
        "filter": "Filter by Category",
        "no_scheme": "No schemes eligible based on provided revenue data."
    },
    "Tamil": {
        "title": "தமிழ்நாடு வருவாய் ஒருங்கிணைந்த திட்ட வரைபடம்",
        "subtitle": "சரிபார்க்கப்பட்ட பயனாளர்களை அரசு நலத்திட்டங்களுடன் இணைக்கிறது",
        "citizen": "குடிமக்கள் விவரங்கள்",
        "check": "தகுதி சரிபார்க்க",
        "eligible": "தகுதியான திட்டங்கள்",
        "search": "திட்டம் தேடுக",
        "filter": "வகை அடிப்படையில் வடிகட்டு",
        "no_scheme": "தரப்பட்ட வருவாய் தகவலின் அடிப்படையில் தகுதியான திட்டங்கள் இல்லை."
    }
}

t = TEXT[language]

# ---------------- CUSTOM UI ----------------
st.markdown(f"""
<style>
.header {{
    background-color:#0E4C92;
    padding:20px;
    border-radius:10px;
    color:white;
    font-size:28px;
    font-weight:bold;
}}
.subtitle {{
    font-size:14px;
    color:gray;
}}
.card {{
    padding:18px;
    border-radius:10px;
    background-color:#f4f8ff;
    margin-bottom:12px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.05);
}}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="header">{t["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{t["subtitle"]}</div>', unsafe_allow_html=True)

schemes = load_schemes()

# ---------------- SIDEBAR FORM ----------------
st.sidebar.header(t["citizen"])

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
district = st.sidebar.text_input("District")

registration_status = st.sidebar.selectbox("Registered in Welfare Board?", ["Yes","No"])

st.sidebar.markdown("---")
st.sidebar.subheader("Revenue Verification")

income_verified = st.sidebar.selectbox("Income Certificate Verified?", ["Yes","No"])
patta_number = st.sidebar.text_input("Patta Number")
caste_certificate = st.sidebar.text_input("Caste Certificate Number")
family_card_number = st.sidebar.text_input("Family Card Number")

# ---------------- BUTTON ----------------
if st.sidebar.button(t["check"]):

    results = find_eligible_schemes(
        age, income, occupation, land, category, gender,
        district, schemes, registration_status,
        income_verified, patta_number,
        caste_certificate, family_card_number
    )

    st.session_state.results = results

# ---------------- DISPLAY RESULTS ----------------
if st.session_state.results:

    st.subheader(t["eligible"])

    df = pd.DataFrame(st.session_state.results, columns=["Scheme","Category"])

    # SEARCH + FILTER
    search = st.text_input(t["search"])
    filter_category = st.selectbox(
        t["filter"],
        ["All"] + list(df["Category"].unique())
    )

    if search:
        df = df[df["Scheme"].str.contains(search, case=False)]

    if filter_category != "All":
        df = df[df["Category"] == filter_category]

    # CARD VIEW
    for index, row in df.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="card">
                <h4>{row['Scheme']}</h4>
                <p><b>Category:</b> {row['Category']}</p>
            </div>
            """, unsafe_allow_html=True)

    # ANALYTICS
    st.subheader("Analytics")
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

elif st.session_state.results == []:
    st.warning(t["no_scheme"])