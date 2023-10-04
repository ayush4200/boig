from file_managment.api import router as file_router
from agent_managment.api import router as agent_router
from chatbots.api import router as chat_router
from prompts.api import router as prompt_router
from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/files/", file_router)
api.add_router("/agents/", agent_router)
api.add_router("/chatbot/", chat_router)
api.add_router("/prompt/", prompt_router)
