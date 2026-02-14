import streamlit as st

if st.session_state.role != "Officer":
    st.warning("Access Denied")
    st.stop()

st.title("Revenue Officer Dashboard")

st.metric("Total Applications Today", 124)
st.metric("Approved", 87)
st.metric("Rejected", 37)

st.bar_chart({
    "Approved": 87,
    "Rejected": 37
})