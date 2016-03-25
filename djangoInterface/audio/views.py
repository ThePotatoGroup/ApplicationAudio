from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import AudioServerModel
from django.shortcuts import render


def index(request):
    return render(request, 'connectionsPage.html', {'connections': AudioServerModel.getConnections()})
    # return HttpResponse("Hello, world. You're at the polls index.")