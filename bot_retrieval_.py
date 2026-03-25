#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# GETTING REQUIRED VARIABLES FROM TOML FILE 
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Backport for older versions

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
# Access specific fields
generation_llm_name_ = data["gemini_llm"]["generation_model_name"]
embedding_llm_name_ = data["gemini_llm"]["embedding_model_name"]
gemini_llm_key_ = data["gemini_llm"]["key_value"]
openai_llm_key_ = data['openai']['openai_key_value']
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA

chroma_path_="./ww2_chroma_db"

google_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", api_key=gemini_llm_key_)
vectorstore = Chroma(persist_directory=chroma_path_)
print("🔄 ChromaDB reloaded successfully!")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-3.1-pro-preview", temperature=0.3, api_key=gemini_llm_key_)

# Create a retrieval-based QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

# Execute a query
# query = "What is the main topic of the document?"
query = "tell me all about Rosie the Riveter "
response = qa_chain.invoke(query)
print(response["result"])


#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# import chromadb
# from chromadb import Documents, EmbeddingFunction, Embeddings
# from google.api_core import retry
# import google.generativeai as genai

# class GeminiEmbeddingFunction(EmbeddingFunction):
#     def __init__(self, document_mode=True):
#         self.document_mode = document_mode

#     def __call__(self, input: Documents) -> Embeddings:
#         task_type = "retrieval_document" if self.document_mode else "retrieval_query"
#         response = genai.embed_content(
#             model="models/text-embedding-004",
#             content=input,
#             task_type=task_type,
#             request_options={"retry": retry.Retry(
#                 predicate=retry.if_transient_error)}
#         )
#         return response["embedding"]
# class DocumentDatabase:
#     def __init__(self, db_name="googlecardb"):
#         self.db_name = db_name
#         self.client = chromadb.Client()

#     def get_db(self, document_mode=True):
#         return self.client.get_or_create_collection(
#             name=self.db_name,
#             embedding_function=GeminiEmbeddingFunction(document_mode)
#         )

#     def store_documents(self, documents):
#         db = self.get_db(True)
#         db.add(documents=documents, ids=[str(i) for i in range(len(documents))])
#         return db.count()

#     def query(self, question):
#         db = self.get_db(False)
#         result = db.query(query_texts=[question], n_results=1)
#         return result["documents"][0][0]
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
    



#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain_chroma import Chroma
# path="./ww2_chroma_db"
# vectorstore = Chroma(persist_directory=path, embedding_function=OpenAIEmbeddings(api_key=openai_llm_key_))
# print("🔄 ChromaDB reloaded successfully!")



# from langchain_classic.chains import RetrievalQA
# retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":5})
# rag_chain = RetrievalQA.from_chain_type(
#     llm= , chain_type="stuff", retriever=retriever, return_source_documents=True)
# query = "tell me all about Rosie the Riveter "
# response = rag_chain.invoke(query)
# print("Answer:", response["result"])



# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
# llm = ChatOpenAI(model_name="gpt-4o", temperature=0, api_key=openai_llm_key_)

# rag_chain = RetrievalQA.from_chain_type(
#     llm=llm, 
#     chain_type="stuff", 
#     retriever=retriever
# )

# 5. Ask a Question
# query = "What is the policy for remote work?"
# response = rag_chain.invoke(query)
# print("Answer:", response["result"])



