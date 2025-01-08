from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
# http://127.0.0.1:8000/openapi.json

app = FastAPI()

### Actual App
from ragAI.ragAI import RagAi

bot = RagAi()
#print(bot.ask("Why is the sky blue?"))
print(bot.get_api_key())
#print(bot.ask_rag("How many words are there?"))

# questions = [
#     "What does Isaiah 58:6-14 say about fasting?",
#     "What does I Kings 21:20-29 say?",
#     "Which verse talks about God bringing gladness to the heart?",
#     "Which verse described a passion for God?",
# ]

# for question in questions:
#     print(f"Question: {question}")
#     print(f"Answer: {bot.ask_rag(question)}")
#     print()

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

@app.get("/api/rag/count-words")
async def rag_root():
    return bot.ask_rag("How many words are there in my text?")

@app.get("/api/rag/{question}")
async def rag_ask(question: str):
    return bot.ask_rag(question)

### TEST
from question.question import Question

@app.post("/api/rag/completions")
async def rag_ask(question: Question):
    return bot.ask_rag(question.text)





### Example
from item.item import Item

items = [Item(text="First task"), Item(text="Second task", is_done=True)]

@app.get("/")
async def root():
    return {"Hello": "World"}

# curl -X POST -H "Content-Type: application/json" -d '{"text":"apple"}' 'http://127.0.0.1:8000/items'
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

# curl -X GET http://127.0.0.1:8000/items?limit=1
@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

# curl -X GET http://127.0.0.1:8000/items/1
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else: 
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

### Example 2
from typing import List
from user.user import User, Gender, Role, UserUpdateRequest
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