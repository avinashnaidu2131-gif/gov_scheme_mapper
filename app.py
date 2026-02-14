import streamlit as st
import requests
from urllib.parse import urlencode

st.set_page_config(page_title="TN Revenue Portal", layout="wide")

# ===== LOAD SECRETS =====
CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

# ===== STATIC REDIRECT (MATCH GOOGLE CONSOLE EXACTLY) =====
REDIRECT_URI = "https://govschememapper-kdtfcxuor89mkd3fy8hrdc.streamlit.app/oauth2callback"

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None


# ================= LOGIN =================
if not st.session_state.user:

    st.title("🔐 Tamil Nadu Revenue Department Portal")

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }

    auth_url = f"{AUTH_URL}?{urlencode(params)}"
    st.markdown(f"[🔑 Login with Google]({auth_url})")

    query_params = st.query_params

    if "code" in query_params:
        code = query_params["code"]

        token_data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_response = requests.post(TOKEN_URL, data=token_data)
        token_json = token_response.json()

        access_token = token_json.get("access_token")

        headers = {"Authorization": f"Bearer {access_token}"}
        user_info = requests.get(USER_INFO_URL, headers=headers).json()

        st.session_state.user = user_info

        if user_info["email"].endswith("@tn.gov.in"):
            st.session_state.role = "Officer"
        else:
            st.session_state.role = "Citizen"

        st.rerun()

    st.stop()


# ================= AFTER LOGIN =================
st.success(f"Logged in as {st.session_state.user['email']}")
st.sidebar.success(f"Role: {st.session_state.role}")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

st.title("Tamil Nadu Government Scheme Mapper")