import requests
from ninja import Router
from typing import Tuple

from qdrant_client import QdrantClient
import os
# from langchain.vectorstores import Qdrant
# from langchain.embeddings import OpenAIEmbeddings

from agent_managment.models import Agent
from prompts.models import Prompt
from chatbots.schemas import ChatIn, ChatOut
from chatbots.langchain_llm.conversation import retrieve_top_k
from chatbots.langchain_llm.conversation import query_llm

router = Router(tags=["chatbots"])


# Get ID, from ID get the collection name using Agent Models. Hit the collection and return if the qdrant client
# succeeded or not
@router.post("/{agent_id}/chat", response=ChatOut)
# def chat(request, agent_id: int):
def chat(request, agent_id: int, prompt_id: int, chat_in: ChatIn) -> Tuple:
    # url = os.environ.get("QUADRANT_URL")
    # api_key = os.environ.get("QUADRANT_API_KEY")
    # openai_api_key = os.environ.get("OPENAI_API_KEY")

    # embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    request.session["chat_in"] = chat_in.chat_in_text
    print(request.session._session_key)

    vector_collection_name = Agent.objects.get(id=agent_id).name

    retrieved_text = retrieve_top_k(chat_in.chat_in_text, vector_collection_name)

    prompt_template_text = Prompt.objects.get(id=prompt_id).text

    chat_out_text = query_llm(prompt_template_text, retrieved_text, chat_in.chat_in_text)

    # collection_info = client.get_collection(collection_name=collection_name)
    # value = collection_info.status.value
    # text = chat_in.chat_text
    # return_text = text + "-" + str(value)

    return 200, {'chat_out_text': chat_out_text}
    # return 200, {"status": value, "message": "Index found and connected"}
