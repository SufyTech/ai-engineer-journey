# day10_app.py - Streamlit AI Chatbot (improved)

import os
import io

import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=API_KEY) if API_KEY else None

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("AI Chatbot")
st.caption("Built by Sufiyan Khan | LLM Post-Training Intern @ Ethara AI")

# ---------- Mode selection ----------
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
    example_prompts = [
        "Summarize this article in 3 bullet points: ",
        "Help me plan a 3-day trip to Goa.",
        "Explain the concept of overfitting in simple terms.",
    ]
elif mode == "Customer Support":
    system_prompt = (
        "You are a polite customer support assistant for an online store. "
        "Ask for missing details, be concise, and keep a friendly tone."
    )
    example_prompts = [
        "I want a refund for my last order.",
        "My payment failed but money was deducted, what should I do?",
        "How can I track my shipment?",
    ]
else:  # Code Helper
    system_prompt = (
        "You are a senior Python developer helping a junior engineer. "
        "Explain step by step, keep examples simple, and mention pitfalls."
    )
    example_prompts = [
        "Explain this error: TypeError: 'NoneType' object is not subscriptable.",
        "Write a Python function to check if a number is prime.",
        "Optimize this loop for performance: ",
    ]

st.caption(f"Mode behavior: {system_prompt}")

# ---------- Session state ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": system_prompt}
    ]

# store feedback as list of dicts aligned with assistant messages
if "feedback" not in st.session_state:
    st.session_state.feedback = []  # each item: {"index": i, "value": "up"/"down"}

# If user changes mode mid-session, reset system message but keep history
if (
    st.session_state.chat_history
    and st.session_state.chat_history[0]["content"] != system_prompt
):
    st.session_state.chat_history[0]["content"] = system_prompt

# ---------- Top controls: clear + mode ----------
top_col1, top_col2 = st.columns(2)
with top_col1:
    if st.button("🧹 Clear chat"):
        st.session_state.chat_history = [
            {"role": "system", "content": system_prompt}
        ]
        st.session_state.feedback = []
with top_col2:
    st.write(f"Mode: **{mode}**")

# ---------- Download button (separate row, easy to see) ----------
if len(st.session_state.chat_history) > 1:
    transcript_lines = []
    for msg in st.session_state.chat_history[1:]:
        speaker = "USER" if msg["role"] == "user" else "ASSISTANT"
        transcript_lines.append(f"{speaker}: {msg['content']}")
    transcript = "\n\n".join(transcript_lines)
    buffer = io.StringIO(transcript)
    st.download_button(
        "📥 Download chat",
        data=buffer.getvalue(),
        file_name="chat_transcript.txt",
        mime="text/plain",
    )

# ---------- Example prompts ----------
with st.expander("Need ideas? Try an example prompt"):
    cols = st.columns(len(example_prompts))
    for i, example in enumerate(example_prompts):
        with cols[i]:
            if st.button(f"Example {i+1}", key=f"example_{mode}_{i}"):
                st.session_state.prefill_prompt = example

# ---------- Render chat history (skip system) + feedback ----------
assistant_index = 0  # to align feedback entries

for msg in st.session_state.chat_history[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        if msg["role"] == "assistant":
            # find existing feedback for this assistant message
            existing = next(
                (f for f in st.session_state.feedback if f["index"] == assistant_index),
                None,
            )
            fb_cols = st.columns(3)
            with fb_cols[0]:
                st.caption("Was this helpful?")
            with fb_cols[1]:
                if st.button("👍", key=f"up_{assistant_index}"):
                    if existing:
                        existing["value"] = "up"
                    else:
                        st.session_state.feedback.append(
                            {"index": assistant_index, "value": "up"}
                        )
            with fb_cols[2]:
                if st.button("👎", key=f"down_{assistant_index}"):
                    if existing:
                        existing["value"] = "down"
                    else:
                        st.session_state.feedback.append(
                            {"index": assistant_index, "value": "down"}
                        )

            # show current feedback status under the message
            existing = next(
                (f for f in st.session_state.feedback if f["index"] == assistant_index),
                None,
            )
            if existing:
                label = (
                    "👍 Marked helpful"
                    if existing["value"] == "up"
                    else "👎 Marked not helpful"
                )
                st.caption(label)

            assistant_index += 1

# ---------- Chat input (form + text_input, supports prefill) ----------
with st.form("chat_form", clear_on_submit=True):
    prompt = st.text_input(
        "Ask me anything...",
        value=st.session_state.get("prefill_prompt", ""),
    )
    submitted = st.form_submit_button("Send")

# clear prefill after using it
if "prefill_prompt" in st.session_state and submitted:
    st.session_state.prefill_prompt = ""

if submitted and prompt.strip():
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    # Call LLM with basic error handling
    if not API_KEY or client is None:
        error_msg = "⚠️ LLM error: GROQ_API_KEY is not set. Please configure your API key."
        st.session_state.chat_history.append(
            {"role": "assistant", "content": error_msg}
        )
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