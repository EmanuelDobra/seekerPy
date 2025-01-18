import ragAI.constants as c
import ragAI.helpers as h
from pydantic import BaseModel
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from operator import itemgetter
from models.question.question import PdfQuestion, RagQuestion
from localEmbeddings import LocalEmbeddings

# Local Models
model = ChatOpenAI(base_url=c.BASE_URL, api_key=c.OPENAI_API_KEY, model=c.GRANITE_MODEL)
embeddings = LocalEmbeddings(url=c.EMBEDDING_URL, model=c.EMBEDDING_MODEL)

# Prompt
parser = StrOutputParser()
prompt = PromptTemplate.from_template(c.TEMPLATE)
prompt.format(context="Here is the context", question="Here is the question")

class RagAi(BaseModel):
    def ask(self, question: str):
        chain = model | parser # Show just string
        # chain = model # Show whole AIMessage
        return chain.invoke(question)
    
    def load_pdfs(self, pdf_name: str = "default.pdf"):
        if ".pdf" not in pdf_name:
            pdf_name += ".pdf"
        loader = PyPDFLoader("./pdfs/" + pdf_name)
        return loader.load_and_split()

    def ask_rag_default(self, question: str):
        pages = self.load_pdfs("default.pdf")
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
    
    def ask_context(self, context: str, question: str):
        chain = prompt | model | parser
        chain.input_schema.model_json_schema()
        chain.invoke({
            "context": {context},
            "question": {question}
        })

# https://www.youtube.com/watch?v=RoR4XJw8wIc
