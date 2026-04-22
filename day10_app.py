# day10_app.py - Streamlit AI Chatbot (improved)

import os

import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY) if API_KEY else None

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("AI Chatbot")
st.caption("Built by Sufiyan Khan | LLM Post-Training Intern @ Ethara AI")

# ----- Mode selection -----
mode = st.selectbox(
    "Choose assistant mode",
    ["General Assistant", "Customer Support", "Code Helper"],
    index=0,
)

if mode == "General Assistant":
    system_prompt = (
        "You are a helpful general AI assistant. "
        "Answer clearly and concisely. Avoid hallucinations; say 'I don't know' if unsure."
    )
elif mode == "Customer Support":
    system_prompt = (
        "You are a polite customer support assistant for an online store. "
        "Ask for missing details, be concise, and keep a friendly tone."
    )
else:  # Code Helper
    system_prompt = (
        "You are a senior Python developer helping a junior engineer. "
        "Explain step by step, keep examples simple, and mention pitfalls."
    )

# ----- Session state -----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": system_prompt}
    ]

# If user changes mode mid-session, reset system message but keep history
if st.session_state.chat_history and st.session_state.chat_history[0]["content"] != system_prompt:
    st.session_state.chat_history[0]["content"] = system_prompt

# Clear chat button
col1, col2 = st.columns(2)
with col1:
    if st.button("🧹 Clear chat"):
        st.session_state.chat_history = [
            {"role": "system", "content": system_prompt}
        ]
with col2:
    st.write(f"Mode: **{mode}**")

# ----- Render chat history (skip system) -----
for msg in st.session_state.chat_history[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ----- Chat input -----
prompt = st.chat_input("Ask me anything...")

if prompt:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Call LLM with basic error handling
    if not API_KEY or client is None:
        error_msg = "⚠️ LLM error: GROQ_API_KEY is not set. Please configure your API key."
        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.write(error_msg)
    else:
        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.chat_history,
                    )

                    reply = response.choices[0].message.content
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": reply}
                    )
                    st.write(reply)

        except Exception as e:
            error_msg = f"⚠️ LLM error: {str(e)}"
            st.session_state.chat_history.append(
                {"role": "assistant", "content": error_msg}
            )
            with st.chat_message("assistant"):
                st.write(error_msg)