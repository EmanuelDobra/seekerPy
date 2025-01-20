from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.question.question import PdfQuestion, RagQuestion
from ragAI.ragAI import RagAi

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
# http://127.0.0.1:8000/openapi.json

app = FastAPI()

# Test LLM works
bot = RagAi()

# Setup CORS
origins = [
    "http://localhost:4200",
    "http://localhost:8080",
    "http://localhost:1234"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get data through url of request
@app.get("/api/rag/{question}")
async def rag_ask_default(question: str):
    return bot.ask_rag_default(question)

# Get data through body of request
@app.post("/api/rag/completions/pdf")
async def rag_ask(pdfQuestion: PdfQuestion):
    return bot.ask_rag_pdf(pdfQuestion)

@app.post("/api/rag/completions/any")
async def rag_ask(ragQuestion: RagQuestion):
    return bot.ask_rag_any(ragQuestion)