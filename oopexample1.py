class ChatUser:
    def __init__(self, name):
        self.name = name
        self.messages = []
        
    def send_message(self, text):
        self.messages.append(text)
        
    def history(self):
        return self.messages
    
    
    
# using the class

user1 = ChatUser("Sufiyan")
user1.send_message("Hi! I am learning OOP in python")
user1.send_message("I want to become a remote AI Engineer")

print("User:", user1.name)
print("History:", user1.history())

