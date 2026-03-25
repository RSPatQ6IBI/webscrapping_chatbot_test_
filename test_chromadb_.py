

import chromadb

# def test_collection_in_chromadb_(chroma_path_="./ww2_chroma_db", collection_name_ = "ww2_articles_collection"):
chroma_path_="./ww2_chroma_db"
collection_name_ = "ww2_articles_collection"
client = chromadb.PersistentClient(path = chroma_path_)
collection = client.get_collection(name=collection_name_)


# According to the documentation https://docs.trychroma.com/usage-guide embeddings are excluded by default for performance:
# When using get or query you can use the include parameter to specify which data you want returned - any of embeddings, documents, metadatas


# Returns a dictionary with keys: 'ids', 'embeddings', 'documents', 'metadatas'
content = collection.get(include=['embeddings', 'documents', 'metadatas'])
print('DOCUMENTS ',10*'-->>',content['documents']) 
print('EMBEDDINGS ',10*'-->>',content['embeddings']) 
