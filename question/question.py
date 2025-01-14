from pydantic import BaseModel

class Question(BaseModel):
    text: str 

class PdfQuestion(BaseModel): 
    question: str
    pdf: str
