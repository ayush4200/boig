from ninja import Schema, ModelSchema
from typing import Optional
from prompts.models import Prompt


class PromptSchema(Schema):
    # class Config:
    #     model = Prompt
    #     model_fields = "__all__"
    id: int
    text: str
    name: str
    metadata: dict
