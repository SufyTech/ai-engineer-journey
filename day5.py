# day5 - Lists and Dictionaries

chat_history = []

def add_message(role,content):
    chat_history.append({"role": role, "content": content})
    
def show_chat_history():
    for msg in chat_history:
        print(f"{msg['role']}: {msg['content']}")

def get_last_message():
    replies = [m for m in chat_history if m['role'] == 'assistant']
    return replies[-1]["content"] if replies else None


add_message("system","You are an RLHF expert")
add_message("user","What is RLHF")
add_message("assistant","RLHF trains LLMs using human feedback")
add_message("user","Who does the rating")
add_message("assistant","Human raters like Sufiyan at Ethara AI")

show_chat_history()
print(f"\nTotal messages: {len(chat_history)}")
print(f"Last reply: {get_last_message()}")