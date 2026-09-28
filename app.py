import os
import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Streamlit Page Config
st.set_page_config(page_title="DevOps Incident AI Agent", page_icon="🛠️", layout="centered")

st.title("🛠️ DevOps Incident Response Agent")
st.caption("Powered by Groq LLM & Hindsight Persistent Memory")

# Setup Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "devops-bank")
HINDSIGHT_BASE_URL = "https://api.hindsight.vectorize.io/v1"

client = Groq(api_key=GROQ_API_KEY)

# Hindsight Functions
def recall_memory(query):
    try:
        headers = {"Authorization": f"Bearer {HINDSIGHT_API_KEY}"} if HINDSIGHT_API_KEY else {}
        res = requests.post(
            f"{HINDSIGHT_BASE_URL}/banks/{HINDSIGHT_BANK_ID}/recall",
            json={"query": query},
            headers=headers,
            timeout=5
        )
        if res.status_code == 200:
            memories = res.json().get("memories", [])
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
    except Exception:
        pass

# Chat History Session Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Past Chat UI Messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User Chat Input UI
if user_input := st.chat_input("Enter server error log or incident details..."):
    # Display User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("Analyzing incident with Hindsight Memory..."):
        # 1. Recall from Hindsight
        context = recall_memory(user_input)
        
        system_instruction = (
            "You are an expert DevOps Incident Response Agent powered by Hindsight persistent memory.\n"
            "Analyze system errors and recommend fixes based on past incident post-mortems.\n"
            f"Relevant Past Memory Context:\n{context}\n"
        )

        # 2. Call Groq LLM
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_input}
            ],
            model="openai/gpt-oss-20b"
        )
        reply = response.choices[0].message.content

        # 3. Retain to Hindsight
        retain_memory(f"User Incident: {user_input} | Agent Solution: {reply}")

    # Display AI Response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)