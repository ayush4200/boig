from django.contrib import admin
from .models import Prompt


# Register your models here.

class PromptAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Prompt._meta.fields]


admin.site.register(Prompt, PromptAdmin)
