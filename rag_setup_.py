
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# DEFINE COLLECTION FOR CHROMADB, TO ADD CONTENT 
import chromadb
chroma_client = chromadb.PersistentClient(path="./ww2_chroma_db")
chroma_collection = chroma_client.get_or_create_collection(name="ww2_articles_collection")
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
gemini_llm_key_ = os.getenv('GEMINI_API_KEY')

#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

def split_the_docs_(all_inp_documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Maximum of 500 characters per chunk
        chunk_overlap=50,  # Overlapping 100 characters to preserve context
        length_function=len,  # Determines chunk size based on character length
        is_separator_regex=False,  # The separator used for splitting is not a regex pattern
    )

    # Merge text data from various sources
    split_documents = text_splitter.split_text(all_inp_documents)
    return text_splitter.create_documents(split_documents)

def get_embeddings_for_text_(document_text_):
    import os 
    from google import genai
    import os
    import numpy as np
    genai_client = genai.Client(api_key=gemini_llm_key_)
    this_doc_embed_ = []
    result = genai_client.models.embed_content(
    model=embedding_llm_name_,
    contents=[
            document_text_
            ] 
    )
    for embeddings_ in result.embeddings:
        this_doc_embed_.append(embeddings_.values)
    return this_doc_embed_

#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# CREATE EMBEDDINGS FOR THE ENTRIES FROM POSTGRE DATABASE, ADD TO CHROMADB 

## THE DATA IS FIRST RETRIEVED FROM THE POSTGRESQL DATABASE, 
from db_operations_postgre_ import fetch_data_from_postgre_
count_ = 0 
arr_primary_key_headings_ = []
arr_article_details = []
data_from_db_ = fetch_data_from_postgre_()
for idx_ in range(int(len(data_from_db_)/2)):
    arr_article_details.append(str(data_from_db_[idx_+int(len(data_from_db_)/2)]))
    arr_primary_key_headings_.append(str(data_from_db_[idx_]))

#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# for articles_ in arr_article_details:
## Choosing only one article --- >>> 
articles_ = arr_article_details[0]
heading_ = arr_primary_key_headings_[0]

## Splitting article --- >>> 
articles_splits_ = split_the_docs_(articles_)
page_heading_embedvec_ = get_embeddings_for_text_(heading_)
# print(f"PAGE HEADING EMBEDDINGS --- >>> ", len(page_heading_embedvec_[0]))
this_metadata_ = [{"source": "title_heading"}]
this_id_ = [ "id_00" ]
chroma_collection.upsert(
    embeddings = page_heading_embedvec_[0],
    documents = [heading_],
    metadatas = this_metadata_,
    ids = this_id_
)

this_splits_embeddings_ = []
count_ = 0.0
for a_split_ in articles_splits_:
    # print(type(str(a_split_)))
    split_embeddings_ = get_embeddings_for_text_(str(a_split_))
    # print(f"SPLIT EMBEDDINGS --- >>> ", len(split_embeddings_[0]))

    if len(this_splits_embeddings_)==0:
        this_splits_embeddings_ = split_embeddings_[0]
    else:
        this_splits_embeddings_ = np.vstack([this_splits_embeddings_, split_embeddings_[0]])
    count_+=1
    this_metadata_ = [{'source':'para_details'+str(float(count_+1)) }]
    this_id_ = [ "id_"+str(float(count_+1)) ]
    chroma_collection.upsert(
        embeddings = split_embeddings_[0],
        documents = [str(a_split_)],
        metadatas = this_metadata_,
        ids = this_id_
    )
    # print('Added to collection --> ', a_split_)
    
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
# CHECK FOR PROPER UPDATE IN COLLECTIONS
# print("TESTING CHROMADB COLLECTION ENTRIES") 
# from test_chromadb_ import test_collection_in_chromadb_ as test_chroma_
# test_chroma_(chroma_client, chroma_collection)
#-_-_-_--_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
