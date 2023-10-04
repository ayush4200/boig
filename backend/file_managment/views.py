from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import Files

# Create your views here.

def index(request):
    return render(request,'index.html',{}) 

def upload(request):
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
        return redirect(upload)
    return render(request,'upload.html',{'form' : UploadForm})