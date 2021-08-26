from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection
from .models import *

# Create your views here.

def login(request):
  if request.method == 'POST':
    print(request.POST)
  return render(request,"login.html")


def signup(request):
  if request.method == 'POST':
    print(request.POST)
  return render(request, "signup.html")


def home(request):
  return render(request, "home.html")



