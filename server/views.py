from django.contrib.auth.models import User, Group
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})

def mainPage(request):
    return render(request, 'mainPage.html',{})