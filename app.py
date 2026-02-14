import streamlit as st
import pandas as pd
from model import find_eligible_schemes
from utils.helpers import load_schemes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- APP CONFIG ----------------
st.set_page_config(page_title="TN Scheme Mapper", layout="wide")

language = st.sidebar.selectbox("Language", ["English", "Tamil"])

if language == "Tamil":
    st.title("தமிழ்நாடு அரசு திட்டங்கள் தகுதி சரிபார்ப்பு")
else:
    st.title("Tamil Nadu Government Scheme Mapper")

schemes = load_schemes()

# ---------------- SIDEBAR INPUTS ----------------
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

# ---------------- ELIGIBILITY ----------------
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
        st.bar_chart(df["Category"].value_counts())

        # PDF GENERATE + DOWNLOAD
        if st.button("Generate PDF Report"):

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
                label="Download PDF",
                data=buffer,
                file_name="eligibility_report.pdf",
                mime="application/pdf"
            )

    else:
        st.warning("No schemes eligible.")