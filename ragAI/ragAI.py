from pydantic import BaseModel
from langchain_openai.chat_models import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
import ragAI.constants as c
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from operator import itemgetter

model = ChatOpenAI(base_url=c.BASE_URL, api_key=c.OPENAI_API_KEY)
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
    
    def load_pdfs(self, pdf_name: str = "manual.pdf"):
        loader = PyPDFLoader(pdf_name)
        return loader.load_and_split()
    
    def ask_context(self, context: str, question: str):
        chain = prompt | model | parser
        chain.input_schema.model_json_schema()
        chain.invoke({
            "context": {context},
            "question": {question}
        })

    def get_documents(self):
        pages = self.load_pdfs()
        vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)
        retriever = vectorstore.as_retriever()
        retriever.invoke("Give me a few passages on fasting")

    def ask_rag(self, question: str):
        pages = self.load_pdfs()
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
    print("WRONG")
