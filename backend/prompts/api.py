import os
from prompts.models import Prompt
from ninja import Router
from ninja import ModelSchema
from typing import List, Tuple, Dict
from prompts.schemas import PromptSchema

router = Router(tags=["prompt"])

# @router.get("/", response=List[AgentOut])
# def list_agents(request):
#     return Agent.objects.all()


# @router.get("/{id}", response=AgentOut)
# def list_agents(request, id: int):
#     return get_object_or_404(Agent, id=id)

@router.post("/create", url_name="prompt_create")
def create_prompt(request, prompt_in: PromptSchema) -> tuple[int, dict]:
    new_prompt = Prompt.objects.create(
        name=prompt_in.name,
        text=prompt_in.text,
        metadata=prompt_in.metadata,
    )

    return 200, {"id": new_prompt.id, "message": "Prompt created successfully"}


@router.get("/list_prompts", response=List[PromptSchema], url_name="get_all_prompts")
def list_prompts(request) -> List[PromptSchema]:
    return Prompt.objects.all()
