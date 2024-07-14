from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
import glob
import toml


class Process_pdf:
    pdf_path = 'data/'
    persist_directory = 'vector_db/'
    chunk_size = 5000
    chunk_overlap = 200

    loaders = []
    def __init__(self):
        for file in glob.glob(os.path.join(self.pdf_path,"*.pdf")):
            self.loaders.append(PyPDFLoader(file))
    
    def store(self):
        docs = []
        for loader in self.loaders:
            print(loader)
            docs.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            length_function=len,
            is_separator_regex=False
        )

        splits = text_splitter.split_documents(docs)
        secrets = toml.load('secrets.toml')
        api_key = secrets['default']['api_key']
        embeddings = OpenAIEmbeddings(api_key=api_key)
        vectordb = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=self.persist_directory
        )
        return vectordb
        
