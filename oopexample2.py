class Chatbot:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt
        self.chat_history = []
        
    def add_user_message(self, text):
        self.chat_history.append({"role": "user", "content": text})
    
    def add_bot_message(self, text):
        self.chat_history.append({"role": "assistant", "content": text})
    
    def get_chat_history(self):
        return self.chat_history
    
bot = Chatbot(
    name = "SupportBot",
    system_prompt = "You are a helpful support assistant."
)

bot.add_user_message("Hi! I need help with my order.")
bot.add_bot_message("Sure! please share your order ID.")
bot.add_user_message("My order ID is 12345.")
bot.add_bot_message("Thank you! I am checking your order details now.")

print("Bot name:", bot.name)
print("System prompt:", bot.system_prompt)
print("Chat history:", bot.get_chat_history())    