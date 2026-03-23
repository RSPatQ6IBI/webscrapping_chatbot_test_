

def get_embeddings_for_text_(document_text_):
    this_doc_embed_ = []
    result = client.models.embed_content(
    model=embedding_llm_name_,
    contents=[
            document_text_
            ] 
    )
    for embeddings_ in result.embeddings:
        this_doc_embed_.append(embeddings_.values)
    return this_doc_embed_


#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
## DEFINE COLLECTION FOR CHROMADB, TO ADD CONTENT 
import chromadb
client = chromadb.PersistentClient(path="./ww2_chroma_db")
collection = client.get_or_create_collection(name="ww2_articles_collection")
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-


#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
## THE DATA IS FIRST RETRIEVED FROM THE POSTGRESQL DATABASE, 
from db_operations_postgre_ import fetch_data_from_postgre_
data_from_db_ = fetch_data_from_postgre_()
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-


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
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# CREATE EMBEDDINGS FOR THE ENTRIES FROM POSTGRE DATABASE, ADD TO CHROMADB 
import os 
from google import genai
import os
import numpy as np
client = genai.Client(api_key=gemini_llm_key_)



for ww2_data_ in data_from_db_:
    page_heading_ = ww2_data_[1]
    page_heading_embedvec_ = get_embeddings_for_text_(page_heading_)
    page_para_abstract_ = ww2_data_[2] 
    page_para_abs_embedvec_ = get_embeddings_for_text_(page_para_abstract_) 
    page_para_details_ = ww2_data_[3] 
    page_para_details_embedvec_ = get_embeddings_for_text_(page_para_details_) 
    id_ = 0.0
    id_+=1
    this_embeddings_ = [np.squeeze(page_heading_embedvec_), np.squeeze(page_para_abs_embedvec_), np.squeeze(page_para_details_embedvec_)]
    
    this_metadatas = [{"source": "title_heading"},{"source": "para_abstract"},{'source':'para_details'}]
    this_ids_ = [ "id_"+str(float(id_+0.1)), "id_"+str(float(id_+0.2)), "id_"+str(float(id_+0.3)) ]
    collection.add(
        embeddings = this_embeddings_,
        documents = [page_heading_, page_para_abstract_, page_para_details_],
        metadatas = this_metadatas,
        ids = this_ids_
    )
    
