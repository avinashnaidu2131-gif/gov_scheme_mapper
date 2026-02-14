import streamlit as st

st.title("Scheme Assistant Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("Ask about schemes...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    if "farmer" in prompt.lower():
        response = "Farmers may be eligible for PM-KISAN and Irrigation Schemes."
    elif "women" in prompt.lower():
        response = "Women may benefit from Free Bus Travel and Magalir schemes."
    elif "fisherman" in prompt.lower():
        response = "Fishermen in Thoothukudi may get Lean Period Assistance."
    else:
        response = "Please enter occupation and district for accurate assistance."

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)