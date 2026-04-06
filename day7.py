# day7.py - APIs 
import requests

def call_api(url):
    try:
        r = requests.get(url,timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
    
    
# Free Joke API

joke = call_api("https://official-joke-api.appspot.com/random_joke")
print(f"Setup:{joke.get('setup')}")
print(f"Punchline:{joke.get('punchline')}")

print("\nTomorrow: OpenAPI API. Same pattern. Real AI!!")