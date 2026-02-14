import streamlit as st
import pandas as pd
from model import find_eligible_schemes
from utils.helpers import load_schemes
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

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
    ["Chennai","Coimbatore","Madurai","Salem","Tirunelveli"]
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

        category_count = df["Category"].value_counts()
        st.bar_chart(category_count)

        # PDF DOWNLOAD
        if st.button("Download PDF Report"):

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            doc = SimpleDocTemplate(temp_file.name)
            elements = []
            styles = getSampleStyleSheet()

            elements.append(Paragraph("Eligible Schemes", styles["Heading1"]))
            elements.append(Spacer(1, 12))

            for scheme in df["Scheme"]:
                elements.append(Paragraph(scheme, styles["Normal"]))
                elements.append(Spacer(1, 6))

            doc.build(elements)

            with open(temp_file.name, "rb") as f:
                st.download_button(
                    "Click to Download",
                    f,
                    file_name="eligibility_report.pdf"
                )

    else:
        st.warning("No schemes eligible.")