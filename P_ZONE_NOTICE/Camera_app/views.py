from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import FileUpload
from PIL import Image
def fileUpload(request):
    if request.method == 'POST':
        # title = request.POST.get('title')
        # content = request.POST.get('content')
        # img = request.FILES.get("imgfile")
        img = request.FILES['Camera']
        # fileupload = FileUpload(
        #     title=title,
        #     content=content,
        #     imgfile=img,
        # )
        # fileupload.save()
        # return redirect('Camera_app:fileupload')
        # return HttpResponse(short)
        img = Image.open(img)
        img.show()
    else:
        fileuploadForm = FileUploadForm
        context = {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)