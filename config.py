import os
from dotenv import load_dotenv

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
hindsight_key = os.getenv("HINDSIGHT_API_KEY")