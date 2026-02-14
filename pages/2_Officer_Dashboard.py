import streamlit as st

st.title("Revenue Officer Dashboard")

st.markdown("""
Officer can:
- Verify Income Certificate
- Verify Patta (Land Record)
- Verify Caste Certificate
- Verify Family Card
""")

income_verified = st.selectbox("Income Certificate Verified?", ["Yes","No"])
patta = st.text_input("Patta Number")
caste = st.text_input("Caste Certificate Number")
family = st.text_input("Family Card Number")

if st.button("Validate Records"):
    st.success("Records Validated Successfully")