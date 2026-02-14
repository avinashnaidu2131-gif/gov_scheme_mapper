import streamlit as st

st.set_page_config(page_title="TN Revenue Portal", layout="wide")

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

# ---------- LOGIN ----------
if not st.session_state.logged_in:

    st.title("🔐 Tamil Nadu Revenue Department Portal")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.session_state.role = "Officer"
            st.rerun()

        elif username == "user" and password == "user123":
            st.session_state.logged_in = True
            st.session_state.role = "Citizen"
            st.rerun()

        else:
            st.error("Invalid credentials")

    st.stop()

st.sidebar.success(f"Logged in as: {st.session_state.role}")
st.title("Tamil Nadu Government Scheme Mapper")
st.info("Use the left sidebar to navigate.")