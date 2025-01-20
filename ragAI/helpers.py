import re
from typing import List
from langchain_core.documents import Document

# Function to chunk text into paragraphs or smaller chunks
def chunk_text(text, chunk_size=512) -> List[Document]:
    # Split text into sentences using a regex
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence)
        if current_length + sentence_length <= chunk_size:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            # Save the current chunk and start a new one
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length

    # Convert each chunk into a Document
    documents = [
        Document(page_content=chunk)
        for i, chunk in enumerate(chunks)
    ]

    return documents