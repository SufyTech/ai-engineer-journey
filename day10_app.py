# day10_app.py  - Streamlit app for day 10

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))    

st.set_page_config(page_title = "AI Chabot", page_icon = "🤖")
st.title("AI Chatbot")
st.caption("Built by Sufiyan Khan | LLM Trainer @ Ethara AI")


if "message" not in st.session_state:
    st.session_state.message = [
        {
            "role":"system",
            "content":"You are a helpful assistant. Answer the user's questions concisely and accurately."
        
        }
    ]


for msg in st.session_state.message[1:]:
    with st.chat_message(msg['role']):
        st.write(msg["content"])
        
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.message.append({"role":"user","content":prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
        
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = st.session_state.message,
    )
    
    reply = response.choices[0].message.content
    st.session_state.message.append({"role":"assistant","content":reply})
    
    with st.chat_message("assistant"):
        st.write(reply)
        
        
        