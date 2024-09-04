import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()

import streamlit as st
st.title("langchain-streamlit-app")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What is up?")
#print(prompt)



if prompt:
    
    st.session_state.messages.append({"role":"user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        #response = "こんにちは"
        #st.markdown(response)
        chat = ChatOpenAI(
            model_name=os.environ["OPENAI_API_MODEL"],
            temperature=os.environ["OPENAI_API_TEMPERATURE"],
        )
        messages = [HumanMessage(content=prompt)]
        response = chat(messages)
        st.markdown(response.content)
        
    st.session_state.messages.append({"role": "assistant", "content": response})