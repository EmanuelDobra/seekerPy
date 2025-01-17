import ragAI.constants as c
from pydantic import BaseModel
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from operator import itemgetter
from models.question.question import PdfQuestion, RagQuestion
import ragAI.helpers as h


from langchain.embeddings.base import Embeddings
from typing import List

# Change embeddings to local one?
# class CustomEmbeddings(Embeddings):
#     def __init__(self, embed_model):
#         self.embed_model = embed_model

#     def embed_documents(self, texts: List[str]) -> List[List[float]]:
#         """Embed a list of documents (strings)."""
#         return [self.embed_model.predict(text) for text in texts]

#     def embed_query(self, text: str) -> List[float]:
#         """Embed a single query."""
#         return self.embed_model.predict(text)
# embedModel = ChatOpenAI(base_url=c.BASE_URL, api_key=c.OPENAI_API_KEY, model="text-embedding-nomic-embed-text-v1.5")
#embeddings = CustomEmbeddings(embed_model=embedModel)

# embeddings = HuggingFaceEmbeddings(model="text-embedding-nomic-embed-text-v1.5")

# Change models if loading multiple: 
model = ChatOpenAI(base_url=c.BASE_URL, api_key=c.OPENAI_API_KEY, model="llama-3.2-1b-instruct")
embeddings = OpenAIEmbeddings()
parser = StrOutputParser()
prompt = PromptTemplate.from_template(c.TEMPLATE)
prompt.format(context="Here is the context", question="Here is the question")

class RagAi(BaseModel):
    def ask(self, question: str):
        chain = model | parser # Show just string
        # chain = model # Show whole AIMessage
        return chain.invoke(question)
    
    def get_api_key(self):
        return c.OPENAI_API_KEY
    
    def load_pdfs(self, pdf_name: str = "default.pdf"):
        if ".pdf" not in pdf_name:
            pdf_name += ".pdf"
        loader = PyPDFLoader("./pdfs/" + pdf_name)
        return loader.load_and_split()
    
    def ask_context(self, context: str, question: str):
        chain = prompt | model | parser
        chain.input_schema.model_json_schema()
        chain.invoke({
            "context": {context},
            "question": {question}
        })

    def ask_rag_default(self, question: str):
        pages = self.load_pdfs("default.pdf")
        vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
        retriever = vectorstore.as_retriever()
        # retriever.invoke("What is the primary point of this text?")
        chain = (
            {
                "context": itemgetter("question") 
                | retriever,
                "question": itemgetter("question")
            }
            | prompt
            | model
            | parser
        )
        return chain.invoke({"question": question})

    def ask_rag_pdf(self, pdfQuestion: PdfQuestion):
        pages = self.load_pdfs(pdfQuestion.pdf or "default.pdf")
        vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
        retriever = vectorstore.as_retriever()
        chain = (
            {
                "context": itemgetter("question") 
                | retriever,
                "question": itemgetter("question")
            }
            | prompt
            | model
            | parser
        )
        return chain.invoke({"question": pdfQuestion.question})

    def ask_rag_any(self, ragQuestion: RagQuestion):
        if ragQuestion.rag_type == "pdf":
            pages = self.load_pdfs(ragQuestion.file_name)
        elif ragQuestion.rag_type == "text":
            pages = h.chunk_text(ragQuestion.context)
        else:
            pages = h.chunk_text(ragQuestion.context)
        vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
        retriever = vectorstore.as_retriever()
        chain = (
            {
                "context": itemgetter("question") 
                | retriever,
                "question": itemgetter("question")
            }
            | prompt
            | model
            | parser
        )
        return chain.invoke({"question": ragQuestion.question})

    def ask_rag_default2(self, question: str):
        pages = h.chunk_text(h.dummy_text())
        vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
        retriever = vectorstore.as_retriever()
        chain = (
            {
                "context": itemgetter("question") 
                | retriever,
                "question": itemgetter("question")
            }
            | prompt
            | model
            | parser
        )
        return chain.invoke({"question": question})

if __name__ == '__main__':
    print("Why?")
