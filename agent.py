import os
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "default")
HINDSIGHT_BASE_URL = "https://api.hindsight.vectorize.io/v1"
client = Groq(api_key = GROQ_API_KEY)

def recall_memory(query):
    try:
        headers = {"Authorization": f"Bearer {HINDSIGHT_API_KEY}"} if HINDSIGHT_API_KEY else {}
        response = requests.post(
            f"{HINDSIGHT_BASE_URL}/banks/{HINDSIGHT_BANK_ID}/recall",
            json={"query": query},
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            memories = response.json().get("memories", [])
            return "\n".join([m.get("text", "") for m in memories])
    except Exception:
        pass
    return ""

def retain_memory(text):
    try:
        headers = {"Authorization": f"Bearer {HINDSIGHT_API_KEY}"} if HINDSIGHT_API_KEY else {}
        requests.post(
            f"{HINDSIGHT_BASE_URL}/banks/{HINDSIGHT_BANK_ID}/retain",
            json={"content": text},
            headers=headers,
            timeout=5
        )
        print("\n[Memory Retained in Hindsight]")
    except Exception:
        pass

def run_agent(user_prompt):
    context = recall_memory(user_prompt)
    
    system_instruction = (
        "You are an intelligent AI assistant with persistent long-term memory powered by Hindsight.\n"
        f"Relevant Past Memory Context:\n{context}\n"
        "Use this memory context whenever relevant to provide personalized answers."
    )
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        model="openai/gpt-oss-20b"
    )
    
    response_text = chat_completion.choices[0].message.content
    retain_memory(f"User said: {user_prompt} | Agent replied: {response_text}")
    return response_text

if __name__ == "__main__":
    print("\n--- Hindsight Powered AI Agent Active ---")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        reply = run_agent(user_input)
        print(f"\nAgent: {reply}\n")