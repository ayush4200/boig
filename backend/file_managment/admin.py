from django.contrib import admin
from .models import DocumentFile


# Define the FileAdmin class
class FileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DocumentFile._meta.fields]

    # make the fields filled automaticly invisible, but ONLY when creating a new object
    # once the object is created, the fields are visible and can be edited (good for debugging)
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # This is the case when creating a new object
            kwargs['exclude'] =  ('size', 'type', 'name', 'location_id')
        return super().get_form(request, obj, **kwargs)

# Register your models here.
admin.site.register(DocumentFile, FileAdmin)