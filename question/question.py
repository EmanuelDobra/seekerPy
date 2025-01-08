from pydantic import BaseModel

class Question(BaseModel):
    text: str 

class Memory(BaseModel): 
    text: str
