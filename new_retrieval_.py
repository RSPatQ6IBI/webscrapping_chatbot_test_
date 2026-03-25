# pip install google-generativeai langchain chromadb pypdf sentence-transformers

from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA

def get_relevant_passage(query, db):
  passage = db.query(query_texts=[query], n_results=1)['documents'][0][0]
  return passage

#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# GETTING REQUIRED VARIABLES FROM TOML FILE 
try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Backport for older versions

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
# Access specific fields
# generation_llm_name_ = data["gemini_llm"]["generation_model_name"]
embedding_llm_name_ = data["gemini_llm"]["embedding_model_name"]
gemini_llm_key_ = data["gemini_llm"]["key_value"]
openai_llm_key_ = data['openai']['openai_key_value']
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
generation_llm_name_= "gemini-2.5-flash" # "gemini-3.1-pro-preview"


from langchain_google_genai import GoogleGenerativeAIEmbeddings
google_embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", api_key=gemini_llm_key_)

chroma_path_="./ww2_chroma_db"
vectorstore = Chroma(persist_directory=chroma_path_, embedding_function = google_embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

print("🔄 ChromaDB reloaded successfully!")
# print(len(retriever._get_relevant_documents("Rosie")))
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
# from langchain.schema.runnable import RunnablePassthrough
# from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Initialize Gemini LLM

llm = ChatGoogleGenerativeAI(model=generation_llm_name_, temperature=0.7, top_p=0.85, api_key=gemini_llm_key_)
llm_prompt_template = """You are an expert on world war 2 facts.
Use the following context to answer the question.
If you don't know the answer, just say that you don't know.
Use five sentences maximum and keep the answer concise.\n
Question: {question} \nContext: {context} \nAnswer:"""

llm_prompt = PromptTemplate.from_template(llm_prompt_template)

# print(llm_prompt)

# Combine data from documents to readable string format.
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | llm_prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke("can you tell broadly about women's role in WWW2 "))
