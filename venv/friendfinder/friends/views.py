from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection
from .models import *

# Create your views here.

def login(request):
  if request.method == 'POST':
    print(request.POST)
    email=request.POST["email"]
    password=request.POST["password"]
    cursor=connection.cursor()
    try:
      cursor.execute("select password from login_detail where email=\'"+email+"\'")
      data=cursor.fetchall()
      if password==data[0][0]:
        return render(request,"home.html")
      else:
        return render(request,"error.html")
    except:
      return render(request,"error.html")
      
  return render(request,"login.html")
    
def signup(request):
  if request.method == 'POST':
    print(request.POST)
    email=request.POST["email"]
    password=request.POST["password"]
    cursor=connection.cursor()
    name=request.POST["name"]
    try:
      cursor.execute("select count(*) from login_detail where email=\'"+email+"\'")
      data=cursor.fetchall()
      print(data)
      if data[0][0]==1:
        return render(request,"error.html")
      else:
        print("insert into login_detail values(5,\'"+name+",\'"+email+"\',\'"+password+"\')")
        cursor.execute("insert into login_detail values(5,\'"+name+"\',\'"+email+"\',\'"+password+"\')")
        return render(request,"success.html")
    except:
      return render(request,"error.html")
  return render(request, "signup.html")

def home(request):
  return render(request, "home.html")



