from langgraph.graph import StateGraph, END
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import Document
from typing import TypedDict, List
import os

class RAGState(TypedDict):
    query: str
    documents: List[Document]
    answer: str

def retrieve(state: RAGState) -> RAGState:
    """Retrieve relevant documents from vector store"""
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.load_local("./vector_store", embeddings)
    docs = vector_store.similarity_search(state["query"], k=3)
    state["documents"] = docs
    return state

def generate(state: RAGState) -> RAGState:
    """Generate answer using retrieved documents"""
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    context = "\n".join([doc.page_content for doc in state["documents"]])
    prompt = f"Context:\n{context}\n\nQuestion: {state['query']}\n\nAnswer:"
    response = llm.invoke(prompt)
    state["answer"] = response.content
    return state

# Build the graph
workflow = StateGraph(RAGState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)
workflow.set_entry_point("retrieve")

rag_chain = workflow.compile()

# Run the RAG pipeline
if __name__ == "__main__":
    result = rag_chain.invoke({"query": "What is machine learning?"})
    print(result["answer"])