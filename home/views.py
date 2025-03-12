from django.shortcuts import HttpResponse, render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'index.html')

def sobre(request):
    return HttpResponse("Sobre o Sistema")