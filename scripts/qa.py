from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_experimental.chat_models import Llama2Chat
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
import toml 

class QA_pdf:
    persist_directory = '../vector_db/'
    vectordb = ''
    llm_name = "gpt-3.5-turbo"
    temperature=0

    def __init__(self, vectordb):
        self.vectordb = vectordb
    
    def _retrieve(self):
        secrets = toml.load('secrets.toml')
        api_key = secrets['default']['api_key']
        llm = ChatOpenAI(model_name=self.llm_name, temperature=self.temperature , api_key=api_key)
        retriever=self.vectordb.as_retriever()
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        qa = ConversationalRetrievalChain.from_llm(
            llm,
            retriever=retriever,
            memory=memory
        )
        return qa
    
    def chat(self, question):
        qa = self._retrieve()
        #retriever=self.vectordb.as_retriever()
        #retrieved_docs = retriever.get_relevant_documents("what was the accuracy achieved for detection?")
        #print("Retrieved contents:")
        #for i, doc in enumerate(retrieved_docs, 1):
        #    print(f"\nDocument {i}:")
        #    print(f"Content: {doc.page_content}")
        #    print(f"Metadata: {doc.metadata}")
        result = qa({"question": str(question)})
        #print(result)
        return result['answer']