from django.db import models


# Create your models here.


class Prompt(models.Model):
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=2000, blank=False, null=False, default="You are a car assistant, you need to "
                                                                              "answer the question based on the "
                                                                              "information given below ")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(blank=True, null=True)
