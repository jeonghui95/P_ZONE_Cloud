import json

import requests
from django.http import HttpResponse
from django.shortcuts import render
from .forms import FileUploadForm
from PIL import Image

def fileUpload(request):
    if request.method == 'POST':
        # title = request.POST.get('title'  )
        # content = request.POST.get('content')
        # img = request.FILES.get("Camera")
        img = request.FILES['Camera']
        # fileupload = FileUpload(
        #     title=title,
        #     content=content,
        #     imgfile=img,
        # )
        # fileupload.save()
        # return redirect('Camera_app:fileupload')


        url = 'http://fastmodel:8000/file/store'
        upload = {'file': img}
        context = requests.post(url,files=upload).json()
        # m = MultipartEncoder(fields=upload)
        # headers = {'Content-Type': m.content_type}
        # res = requests.post(url, headers=headers, data=m)

        # context = json.load(res)
        return render(request,'result.html',context)




    else:
        fileuploadForm = FileUploadForm
        context = {

            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'fileupload.html', context)
# @csrf_exempt
# def imageview(request):
#     # return HttpResponse("HI")
#     if request.method == 'POST':
#         img = request.FILES["media"]
#         img = Image.open(img)
#         img.show()