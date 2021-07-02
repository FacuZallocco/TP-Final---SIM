from django.shortcuts import render
from django.views import generic
import random, math

# Create your views here.

def index(request):
    return render(request, "index.html")

def acercade(request):
    return render(request, "acercade.html")