from langchain.document_loaders import JSONLoader
from langchain.document_loaders import DirectoryLoader
import os
from pathlib import Path
import json
from pprint import pprint
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from langchain.chains.question_answering import load_qa_chain


# Get the current directory
current_dir = os.getcwd()
# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Specify the folder name within the grandparent directory
folder_name = "media/files"

# Get the path of the folder within the grandparent directory
media_path = os.path.join(parent_dir, folder_name)


# Data Loader

file_path = os.path.join(media_path,"20201102_IPA_QA_en-US.json")
data = json.loads(Path(file_path).read_text())
#pprint(data)

loader = JSONLoader(
    file_path=file_path,
    jq_schema='.data[].paragraph[].context')

data = loader.load()



#Splitting the Data (documents) into chunks. Could be skipped since JSON loader already loads it into multiple documents

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 250,
    chunk_overlap  = 30,
    length_function = len,
    add_start_index = True
)

texts = text_splitter.split_documents(data)



embeddings = OpenAIEmbeddings()
db_index = Chroma.from_documents(texts,embeddings, collection_name = "chroma_index")



def get_similar_docs(query, k = 2, score = False):
    if score:
        similar_docs = db_index.similarity_search_with_score(query, k =k)
    else:
        similar_docs =  db_index.similarity_search(query, k = k)
    return similar_docs


chat_llm = OpenAI(temperature = 0)
chain = load_qa_chain(chat_llm, chain_type="stuff")

def get_answer(query):
    similar_docs = get_similar_docs(query, 3,False)
    answer = chain.run(input_documents=similar_docs, question=query)
    return answer