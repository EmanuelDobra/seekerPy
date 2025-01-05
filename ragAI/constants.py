import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "llama-3.2-1b-instruct"
BASE_URL = "http://localhost:1234/v1"
TEMPLATE = """
Try your best to answer within context. Always add the name of the one to whom the quot belongs.

Context: {context}

Question: {question}
"""