from django.conf import settings
from django.db import models
from bmw_llm_dms.common.utils.user_utils import get_standard_user

# Create your models here.

from file_managment.models import DocumentFile
from prompts.models import Prompt


class Agent(models.Model):
    class DeploymentStatus(models.IntegerChoices):
        PENDING = 1
        DEPLOYED = 2
        FAILED = 3

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    greeting = models.CharField(max_length=200, blank=True, null=True, default="Hi, how can I help you?")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,  # if the user is deleted do "nothing"
        blank=True,
        default=get_standard_user)
    files = models.ManyToManyField(DocumentFile)
    prompt = models.ForeignKey(Prompt, on_delete=models.PROTECT, blank=True, null=True)
    vector_index_name = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    chatbot_frontend_url = models.CharField(max_length=200, blank=True, null=True)
    chatbot_api_url = models.CharField(max_length=200, blank=True, null=True)
    deployment_status = models.IntegerField(choices=DeploymentStatus.choices, default=DeploymentStatus.PENDING)
    metadata = models.JSONField(blank=True, null=True)
