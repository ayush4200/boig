from django.forms import ModelForm
from django import forms
from .models import Files


# Ties the form information with the "model" we have created in models.py
class UploadForm(ModelForm):
    filename = forms.TextInput()
    file = forms.FileField()

    class Meta:
        model = Files
        fields = ['filename', 'file']
