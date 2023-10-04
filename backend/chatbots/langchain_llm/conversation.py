import os
from os import environ as env
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings

from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

import openai


def _get_qdrant_client() -> QdrantClient:
    url = env.get("QUADRANT_URL")
    api_key = env.get("QUADRANT_API_KEY")

    return QdrantClient(
        url=url,
        api_key=api_key,
        prefer_grpc=True
    )


def retrieve_top_k(query_in: str, vector_collection_name: str, k: int = 1) -> str:
    embeddings = OpenAIEmbeddings(openai_api_key=env.get("OPENAI_API_KEY"))

    qdrant = Qdrant(client=_get_qdrant_client(), collection_name=vector_collection_name, embeddings=embeddings)

    retrieved_docs = qdrant.similarity_search_with_score(query_in, k=k)
    retrieved_text = str()
    for doc in retrieved_docs:
        retrieved_text = doc[0].page_content

    return retrieved_text


def query_llm(prompt_template_text: str, retrieved_text: str, query_in: str) -> str:
    openai.api_key = env.get("OPENAI_API_KEY")
    completion = openai.ChatCompletion()
    message_log = [{
        'role': 'system',
        'content': f'{prompt_template_text}\n\nContext:\n{retrieved_text}',
    }, {'role': 'user', 'content': query_in}]
    response = completion.create(model='gpt-4', messages=message_log, temperature=0.2)
    answer = response.choices[0]['message']['content']
    # prompt = PromptTemplate(input_variables=["context", "human_input"], template=prompt_template_text)
    return answer
