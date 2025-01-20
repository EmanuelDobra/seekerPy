from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.question.question import PdfQuestion, RagQuestion
from ragAI.ragAI import RagAi

# Useful
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

### Python FastApi Tutorial ###
from typing import List
from models.user.user import User, Gender, Role, UserUpdateRequest
from uuid import UUID

db: List[User] = [
    User(id=UUID("b78de049-51b4-486a-9dd6-c1f18498d56c"), name="Kale", nickname="Kay", gender=Gender.male, roles=[Role.admin]),
    User(id=UUID("e032ecaf-3345-404d-8dc7-b4017d348243"), name="Frank", gender=Gender.male, roles=[Role.admin])
]

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id, "name": user.name}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
        raise HTTPException(status_code=404, detail=f"user with id: {user_id} does not exist")

# Override user with another given with same id
@app.put("/api/v1/users")
async def update_user(user: User):
    for usr in db:
        if (usr.id == user.id):
            usr.gender = user.gender
            usr.name = user.name
            usr.nickname = user.nickname
            usr.roles = user.roles
            return
        raise HTTPException(status_code=404, detail=f"user with id: {user.id} does not exist")

# Override user with given update request if user id provided exists
@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if (user.id == user_id):
            user.gender = user_update.gender or user.gender
            user.name = user_update.name or user.name
            user.nickname = user_update.nickname or user.nickname
            user.roles = user_update.roles or user.roles
            return
        raise HTTPException(status_code=404, detail=f"user with id: {user.id} does not exist")