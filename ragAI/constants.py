import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = ""
BASE_URL = "http://localhost:1234/v1"
EMBEDDING_URL = "http://localhost:1234/v1/embeddings"
GRANITE_MODEL = "granite-3.1-8b-instruct"
LLAMA_MODEL = "llama-3.2-1b-instruct"
QUEN_MODEL = "qwen2.5-7b-instruct"
EMBEDDING_MODEL = "text-embedding-nomic-embed-text-v1.5"
TEMPLATE = """
Speak English please. Always answer within context. If you cannot find any information about the question, respond with "## I don't know".
ALWAYS RESPOND USING MARKDOWN NOTATION. Make a title with ##, and bold or italicize important texts. Try to use bullet points when possible.

Context: {context}

Question: {question}
"""