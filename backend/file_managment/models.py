# Create your models here.
from django.db import models
from django.conf import settings
from bmw_llm_dms.common.utils.user_utils import get_standard_user


class DocumentFile(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    uploaded_file = models.FileField(upload_to='files/')  # TODO: use some temp folder and then "pipe" it to S3 or so.
    type = models.CharField(max_length=50, blank=True, null=True)
    location_id = models.CharField(max_length=200, blank=True, null=True)
    size = models.FloatField(blank=True, null=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        blank=True,
        default=get_standard_user)  # if the user is deleted do "nothing"
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Overriding the save method to update the name, type and size
        of the file before saving it
        """
        # The file has been saved at this point, so we can access it

        self.name = self.name or self.uploaded_file.name
        self.size = self.uploaded_file.size
        self.type = self.type or self.uploaded_file.file.content_type

        super(DocumentFile, self).save(*args, **kwargs)  # Call the "real" save() method


class Files(models.Model):
    filename = models.CharField(max_length=200)
    file = models.FileField(upload_to="files/")
