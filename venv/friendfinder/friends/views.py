from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection

# Create your views here.

def login(request):
  
  #POST request
  if request.method == 'POST':
    #Storing data entered by user in variables
    email=request.POST["email"]
    password=request.POST["password"]

    #MySQL cursor initialization
    cursor=connection.cursor()

    #Try block is used to catch errors in database connection
    try:
      #Get password corresponding to email from database
      cursor.execute("select password from login_detail where email=\'"+email+"\'")

      #Store it in data
      data=cursor.fetchall()

      #Compare user entered password and password in database
      #data[0][0] is used because password is of the form (("***"),)
      if password==data[0][0]:
        
        #If passwords match allow user to enter home-page
        return render(request,"home.html")
      
      else:
        #If passwords dont match, show error page
        return render(request,"error.html")
      
    except:
      return render(request,"error.html")
  #GET request    
  return render(request,"login.html")
    
def signup(request):
  
  #POST request
  if request.method == 'POST':
    #Storing data entered by user in variables
    email=request.POST["email"]
    password=request.POST["password"]
    name=request.POST["name"]
    
    #MySQL cursor initialization
    cursor=connection.cursor()
    
    try:
      
      #Check if entered email already exists in database
      cursor.execute("select count(*) from login_detail where email=\'"+email+"\'")
      data=cursor.fetchall()
      
      if data[0][0]==1:
        #If exists, send error
        return render(request,"error.html")
      
      else:
        #If does not exist, add new details into database
        cursor.execute("insert into login_detail values(5,\'"+name+"\',\'"+email+"\',\'"+password+"\')")

        #Show user that signup has been completed
        return render(request,"success.html")
    except:
      return render(request,"error.html")
    
  #GET request   
  return render(request, "signup.html")

def home(request):
  return render(request, "home.html")



