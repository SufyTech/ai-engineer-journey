from groq import Groq
from dotenv import load_dotenv
import os,json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_history = [
    {"role":"system","content":"You are an expert In AI and RLHF. Be helpful and concise."},
]

def chat(user_message):
    chat_history.append({"role":"user","content":user_message})
    
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = chat_history,
    )
    
    reply = response.choices[0].message.content
    chat_history.append({"role":"assistant","content":reply})
    return reply

# Test conversation

print("AI:", chat("What is RLHF"))
print("AI:", chat("Who does the human feedback part?"))
print("AI:", chat("What are the benefits of RLHF?"))

# Save the chat history to a file

with open("chat_session.json", "w") as f:
    json.dump(chat_history, f, indent=2)
print("\nConversation saved!")

