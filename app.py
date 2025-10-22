import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from utils import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

def user_input_handler(question):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = db.similarity_search(question)
    
    chain = get_conversational_chain()
    
    response = chain.invoke({"context": docs, "question": question})
    
    st.markdown("### 💡 Answer")
    st.markdown(response)  # Response is now a string directly
    
    with st.expander("📄 View matched context from your PDF"):
        for i, doc in enumerate(docs):
            st.markdown(f"**Chunk {i+1}:**")
            st.markdown(f"``````")

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
