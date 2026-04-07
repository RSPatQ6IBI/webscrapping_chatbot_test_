
#___________________________________________________#
# CHECKING THE COLLECTION 
'''
import chromadb
chroma_path_="./ww2_chroma_db"
collection_name_ = "ww2_articles_collection"
client = chromadb.PersistentClient(path = chroma_path_)
collection = client.get_collection(name=collection_name_)
print(10*'-<>-','\n\n', "--- TESTING COLLECTION FROM CHROMADB , LOCATED AT ---", chroma_path_)

# According to the documentation https://docs.trychroma.com/usage-guide embeddings are excluded by default for performance:
# When using get or query you can use the include parameter to specify which data you want returned - any of embeddings, documents, metadatas


# Returns a dictionary with keys: 'ids', 'embeddings', 'documents', 'metadatas'
content = collection.get(include=['embeddings', 'documents', 'metadatas'])
for an_cembedding_ in content['embeddings']:
    print(an_cembedding_.shape)
    print('\n\n', 10*'-->>' )

# print('DOCUMENTS ',10*'-->>',content['documents']) 
# print('EMBEDDINGS ',10*'-->>',content['embeddings']) 
# print('METADATAS ',10*'-->>',content['metadatas']) 
'''

#___________________________________________________#
# QUERYING THE COLLECTION 
'''
print(10*'-<>-','\n\n', "--- QUERYING COLLECTION FROM CHROMADB , LOCATED AT ---", chroma_path_)

query_text_="what happened in war" 
from rag_setup_ import get_embeddings_for_text_
import numpy as np
query_embed_ = get_embeddings_for_text_(query_text_)
res_ = collection.query(query_embeddings = query_embed_,n_results=2)
res_ = res_['documents'] 
for a_res_ in res_:
    print(a_res_,'\n\n\n')

'''

#___________________________________________________#
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.retrievers import MultiQueryRetriever
from rag_setup_ import get_embeddings_for_text_
import numpy as np

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Backport for older versions

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
# Access specific fields
generation_llm_name_ = data["gemini_llm"]["generation_model_name"]
embedding_llm_name_ = data["gemini_llm"]["embedding_model_name"]
gemini_llm_key_ = os.getenv('GEMINI_API_KEY')


google_embeddings = GoogleGenerativeAIEmbeddings(model=embedding_llm_name_, api_key=gemini_llm_key_)
chroma_path_="./ww2_chroma_db"
vectorstore = Chroma(persist_directory=chroma_path_, embedding_function = google_embeddings)
# vectorstore = Chroma(persist_directory=chroma_path_, embedding_function = get_embeddings_for_text_)
the_query_ = "who is Rosie"
the_llm = ChatGoogleGenerativeAI(model=generation_llm_name_, temperature=0.7, top_p=0.85, api_key=gemini_llm_key_)
mq_retriever = MultiQueryRetriever.from_llm(retriever = vectorstore.as_retriever(), llm = the_llm)
retrieved_docs = mq_retriever.invoke(the_query_)
print(retrieved_docs)

# Similarity search with query
# matched_docs = vectorstore.similarity_search(query = the_query_, k = 3)
# print(matched_docs)
# print(vectorstore)

# the_llm = ChatGoogleGenerativeAI(model=generation_llm_name_, temperature=0.7, top_p=0.85, api_key=gemini_llm_key_)


# mq_retriever = MultiQueryRetriever.from_llm(retriever = vectorstore.as_retriever(), llm = the_llm)
# query = "what is the document about"
# retrieved_docs = mq_retriever.invoke(query)
# print(retrieved_docs)

#___________________________________________________#
