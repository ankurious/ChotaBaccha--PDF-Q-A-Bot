# import streamlit as st
# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# import os
#
# # Load API key
# load_dotenv()
# groq_api_key = os.getenv("GROQ_API_KEY")
#
# # Basic functions
# def get_pdf_text(pdf_docs):
#     text = ""
#     for pdf in pdf_docs:
#         reader = PdfReader(pdf)
#         for page in reader.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text
#     return text
#
# def get_text_chunks(text):
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     return splitter.split_text(text)
#
# def get_vector_store(chunks):
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
#     vectorstore.save_local("faiss_index")
#
# def get_conversational_chain():
#     prompt_template = """
#     Answer the question based on the context below. If you can't find the answer, say "Answer not available in the context."
#
#     Context: {context}
#     Question: {question}
#
#     Answer:
#     """
#     prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
#     llm = ChatGroq(model_name="llama3-8b-8192", groq_api_key=groq_api_key)
#     return load_qa_chain(llm, chain_type="stuff", prompt=prompt)
#
# def user_input_handler(question):
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
#     docs = db.similarity_search(question)
#     chain = get_conversational_chain()
#     response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
#     st.write("**Answer:**", response["output_text"])
#
# # Streamlit UI
# def main():
#     st.set_page_config(page_title="Chat with your PDFs")
#     st.title("📝 Chat with your PDF (Free Groq + HF Setup)")
#
#     with st.sidebar:
#         pdf_docs = st.file_uploader("Upload PDFs", accept_multiple_files=True)
#         if st.button("Process PDFs") and pdf_docs:
#             with st.spinner("Reading and processing..."):
#                 text = get_pdf_text(pdf_docs)
#                 chunks = get_text_chunks(text)
#                 get_vector_store(chunks)
#                 st.success("✅ Processing done!")
#
#     question = st.text_input("Ask a question from your PDF:")
#     if question:
#         user_input_handler(question)
#
# if __name__ == "__main__":
#     main()


import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from utils import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

def user_input_handler(question):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = db.similarity_search(question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)

    st.markdown("### 💡 Answer")
    st.markdown(response["output_text"])




    with st.expander("🗂️ Source documents used"):
        for i, doc in enumerate(docs):
            st.markdown(f"**Doc {i+1}**")
            st.write(doc.page_content[:500] + "...")

def main():
    st.set_page_config(page_title="📚 PDF, BotKiBaat", layout="wide")
    st.title("📝 ChotaBacchaPDF, EkBotKatha")

    with st.sidebar:
        st.header("📂 Upload your bada baccha here")
        pdf_docs = st.file_uploader("Choose files", accept_multiple_files=True, type=["pdf"])
        if pdf_docs:
            st.markdown("**Uploaded Files:**")
            for pdf in pdf_docs:
                st.write("📄", pdf.name)

        if st.button("📊 Process PDFs") and pdf_docs:
            with st.spinner("📖 Reading & indexing..."):
                raw_text = get_pdf_text(pdf_docs)
                chunks = get_text_chunks(raw_text)
                get_vector_store(chunks)
                st.success("✅ PDFs processed and indexed!")

    st.markdown("---")
    st.subheader("🔍 Ask something from your PDFs")

    question = st.text_input("🗨️ Aapki Zarurat")
    if question:
        user_input_handler(question)

if __name__ == "__main__":
    main()
