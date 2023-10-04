import os
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from agent_managment.models import Agent
from ninja import Router
from ninja import ModelSchema
from typing import List

from agent_managment.schemas import AgentOut, AgentIn
from bmw_llm_dms.common.schemas import UserOutSchema
from bmw_llm_dms.common.utils.user_utils import get_standard_user
from file_managment.api import FileSchema
from file_managment.models import DocumentFile
from prompts.models import Prompt
from agent_managment.ingestion_task import ingest_docs


# everything in thi file will be on /api/agents/
router = Router(tags=["agents"])


##############################
# Routes for the agent model #
##############################

# TODO: LATER add pagination to this route
@router.get("/", response=List[AgentOut])
def list_agents(request):
    # agent_list = list()
    # agents = Agent.objects.all()
    # for agent in agents:
    #     agent.file_count = agent.files.count()
    #     agent_list.append(agent)
    return Agent.objects.all()
    # return agent_list


@router.get("/{id}", response=AgentOut)
def list_agents(request, id: int):
    return get_object_or_404(Agent, id=id)

@router.post("/", url_name="agent_create")
def create_agent(request, agent_in: AgentIn):
    try:
        user = User.objects.get(id=agent_in.user) or User.objects.get(pk=get_standard_user())
    except User.DoesNotExist:
        raise Http404("User does not exist")

    new_agent = Agent.objects.create(
        user=user,
        name=agent_in.name,
        prompt=get_object_or_404(Prompt, id=agent_in.prompt),
        greeting=agent_in.greeting,
        metadata=agent_in.metadata,

    )

    print(os.getcwd())
    # parent_dir = os.path.dirname(os.getcwd())

    # media_path = "/backend/media/files"
    # media_path = os.path.join(parent_dir, folder_name)

    # If files are provided, add them to the 'files' field
    if agent_in.files is not None:

        new_agent.metadata["file_count"] = len(agent_in.files)
        for file_id in agent_in.files:
            new_agent.files.add(
                get_object_or_404(DocumentFile, id=file_id)
            )

        file_objs = DocumentFile.objects.filter(id__in=agent_in.files)
        uploaded_file_paths = [file_obj.uploaded_file.path for file_obj in file_objs]
        # file_names = [os.path.basename(up_file_obj.name) for up_file_obj in uploaded_file_names]
        new_agent.save()

        ingest_docs(files=uploaded_file_paths,
                    agent=new_agent)

    else:
        Http404("No files provided")

    #
    # if agent_in.prompts is not None:

    return 200, {"id": new_agent.id, "message": "Agent created successfully"}


# This implementation is good!
@router.delete("/{id}", response={200: dict, 404: None})
def delete_agent(request, id):
    agent_to_delete = get_object_or_404(Agent, id=id)
    agent_id = agent_to_delete.id
    agent_to_delete.delete()
    return 200, {"id": agent_id, "message": "Agent deleted successfully"}
