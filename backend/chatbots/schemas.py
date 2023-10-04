from ninja import NinjaAPI, File, Schema, ModelSchema
from typing import Optional

# from agent_managment.models import Agent
# from bmw_llm_dms.common.schemas import UserOutSchema
# from bmw_llm_dms.common.utils.user_utils import get_standard_user
# from file_managment.api import FileSchema


###############################
# Schemas for the agent model #
###############################
class ChatOut(Schema):
    chat_out_text: str


class ChatIn(Schema):
    chat_in_text: str
    metadata: Optional[dict]
