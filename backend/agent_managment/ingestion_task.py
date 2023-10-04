# Note: Splitting the Data (documents) into chunks. Could be skipped since JSON loader already loads it
# into multiple documents; chunk size should be a hyperparameter which the user can control depending on the documents
import logging
import os
from typing import List
from django_huey import task
from langchain.document_loaders import JSONLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant
from agent_managment.models import Agent


@task(retries=2)
def ingest_docs(files: List, agent: Agent):
    # Initialise text_splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=30, length_function=len,
                                                   add_start_index=False)

    # Data Loader, docs
    loaders = [None] * len(files)
    docs = [None] * len(files)
    texts = [None] * len(files)

    for idx, file in enumerate(files):
        loaders[idx] = JSONLoader(file_path=file, jq_schema='.data[].paragraphs[].context')

        docs[idx] = loaders[idx].load()

        texts[idx] = text_splitter.split_documents(docs[idx])

    merged_texts = []
    for sublist in texts:
        merged_texts.extend(sublist)

    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key is not None:
        logging.info("OPENAI key retrieved..")

    embeddings_generator = OpenAIEmbeddings(openai_api_key=openai_api_key)

    url = os.environ.get("QUADRANT_URL")
    quad_api_key = os.environ.get("QUADRANT_API_KEY")

    logging.info("Loading documents to Qdrant and creating index")

    Qdrant.from_documents(documents=merged_texts, embedding=embeddings_generator, url=url,
                          prefer_grpc=True, api_key=quad_api_key, collection_name=agent.name)

    print("Index created\n")
    agent.deployment_status = agent.DeploymentStatus.DEPLOYED
    agent.save()
