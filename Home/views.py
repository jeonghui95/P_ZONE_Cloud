from django.shortcuts import render

# Create your views here.


def Index(request):
    context={}
    return render(request,'Home.html',context)