import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI Key is not set")

METADATA_MODEL = os.getenv("METADATA_MODEL", "gpt-4.1-mini")