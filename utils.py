from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chains import load_qa_chain  # ✅ Correct import for LangChain ≥ 0.3
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def get_text_chunks(text):
    """Split extracted text into overlapping chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)


def get_vector_store(chunks):
    """Embed and store text chunks in a FAISS vector database."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    vectorstore.save_local("faiss_index")


def get_conversational_chain():
    """Create a question-answering chain using Groq's LLaMA model."""
    prompt_template = """
    Answer the question based on the context below. 
    If you can't find the answer, say "Answer not available in the context."

    Context: {context}
    Question: {question}

    Answer:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=groq_api_key)
    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    return chain
