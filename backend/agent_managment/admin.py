from django.contrib import admin
from .models import Agent

class AgentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Agent._meta.fields]


# Register your models here.
admin.site.register(Agent, AgentAdmin)