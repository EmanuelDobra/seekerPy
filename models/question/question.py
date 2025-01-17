from pydantic import BaseModel

class Question(BaseModel):
    text: str 

class PdfQuestion(BaseModel): 
    question: str
    pdf: str

class RagQuestion(BaseModel):
    question: str
    rag_type: str
    context: str = ""
    file_name: str = "default.pdf"