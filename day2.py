# Day2 - String

prompt = "What is machine learning?"
response = "RLHF trains LLMs using human feeback"   

print(prompt.strip())
print(prompt.strip().upper())
print(prompt.strip().replace("machine learning","RLHF"))

words = len(prompt.split())
print(f"words : {words}")

topic = "RLHF"
my_prompt = f"Explain {topic} in simple terms:"
print(f"Prompt : {my_prompt}")
