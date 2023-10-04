from typing import List, Dict

from django.shortcuts import get_object_or_404
from ninja import ModelSchema, NinjaAPI, File
from ninja.files import UploadedFile
from django.conf import settings
from file_managment.models import DocumentFile
from ninja import Router

router = Router(tags=["files"])


###############################
# Schemas for the file model #
###############################

class FileSchema(ModelSchema):
    class Config:
        model = DocumentFile
        model_fields = "__all__"


# TODO define this schemas
FileIn = FileSchema
FileOut = FileSchema


######################
# Routes for the file #
######################

@router.post("/upload", url_name="upload")
def upload(request, file: UploadedFile = File(...)):
    doc_file = DocumentFile.objects.create(uploaded_file=file)
    doc_file.save()
    return {'file_id': doc_file.id, 'name': file.name}


@router.get("/files", url_name="files", response=List[FileOut])
def get_files(request) -> List[FileOut]:
    return DocumentFile.objects.all()


@router.delete("/delete-files", url_name='delete', response={200: dict, 404: None})
def delete_files(request, file_id_to_del: List[int]) -> Dict:
    deleted_files = []
    for file_id in file_id_to_del:
        file_to_delete = get_object_or_404(DocumentFile, id=file_id)
        file_delete_id = file_to_delete.id
        file_to_delete.delete()
        deleted_files.append(file_delete_id)
    return {"id": deleted_files, "message": "File deleted successfully"}
