import streamlit as st
import random
from services.services import agent
from services.file import upload_to_qdrant
import time



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_name" not in st.session_state:
    st.session_state.file_name = ""
# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
uploaded_file = st.file_uploader("📄 Upload a PDF to embed into Qdrant", type=["pdf"], key='pdf-uploader')
if uploaded_file and not uploaded_file.name == st.session_state.file_name:
    with st.spinner("Processing and uploading to Qdrant..."):
        success, msg = upload_to_qdrant(uploaded_file.read())
        #add insert logic here
    st.session_state.file_name = uploaded_file.name
    st.success(msg)
# Chat input
if prompt := st.chat_input("Ask me anything!"):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot reply with a random number
    reply = agent.get_bot_response(prompt, st.session_state.messages[:-1])
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)


