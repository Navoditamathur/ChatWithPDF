import streamlit as st
from scripts.processing import Process_pdf
from scripts.qa import QA_pdf
import os
import shutil

# Directory to save uploaded files
UPLOAD_FOLDER = 'data/'
VECTOR_DB_FOLDER = 'vector_db/'

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)

st.title("Chat with PDF")
if 'file_uploader_key' not in st.session_state:
    st.session_state['file_uploader_key'] = 0

if 'uploaded_files' not in st.session_state:
    st.session_state['uploaded_files'] = []

def save_uploaded_files(uploaded_files):
    saved_file_paths = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_file_paths.append(file_path)
    return saved_file_paths

# Function to delete files and reset the app
def reset_app():
    if os.path.exists(UPLOAD_FOLDER):
        shutil.rmtree(UPLOAD_FOLDER)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    if os.path.exists(VECTOR_DB_FOLDER):
        shutil.rmtree(VECTOR_DB_FOLDER)
    os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)
    # Clear session state
    for key in st.session_state.keys():
        print(key)
        if key == 'file_uploader_key':
            st.session_state[key]+=1
        else:
            del st.session_state[key]
    processed_pdfs.loaders = []
    st.rerun()

# File uploader for PDF
uploaded_pdfs = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key=st.session_state['file_uploader_key'])

if uploaded_pdfs:
    # Display a progress indicator while files are being uploaded
    with st.spinner('Uploading files...'):
        saved_file_paths = save_uploaded_files(uploaded_pdfs)
        st.session_state['uploaded_files'] = uploaded_pdfs
        st.success("Files uploaded successfully")
    
    with st.spinner('Processing...'):
    # Process PDFs and load vector database
        processed_pdfs = Process_pdf()
        vector_db = processed_pdfs.store()
    
        # Initialize QA system
        qa = QA_pdf(vector_db)
    
    # Text input for asking questions
    question = st.text_input("Ask a question about the uploaded PDFs (Press enter):", key="input")
    
    if question:
        # Display a spinner while generating the answer
        with st.spinner('Generating answer...'):
            # Get answer from QA system
            answer = qa.chat(question)
        
            # Display question and answer
            st.write("Question:", question)
            st.text_area("Answer", answer, height=300, key = "answer")

# Add a button to reset the app
if st.button("Reset"):
    with st.spinner('Loading...'):
        reset_app()