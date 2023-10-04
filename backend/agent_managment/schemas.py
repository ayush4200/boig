from ninja import Schema
from typing import List, Optional

from bmw_llm_dms.common.schemas import UserOutSchema
from bmw_llm_dms.common.utils.user_utils import get_standard_user
from file_managment.api import FileSchema
from prompts.schemas import PromptSchema


###############################
# Schemas for the agent model #
###############################
class AgentOut(Schema):
    id: int
    name: str
    files: List[FileSchema]
    prompt: PromptSchema
    user: UserOutSchema = None
    metadata: dict
    chatbot_api_url: Optional[str]
    chatbot_frontend_url: Optional[str]
    deployment_status: Optional[int]


class AgentIn(Schema):
    files: List[int]
    user: int = get_standard_user()
    name: str
    prompt: int
    greeting: Optional[str]
    metadata: Optional[dict]
