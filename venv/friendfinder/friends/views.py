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
      cursor.execute("select password from friends_login_detail where email=\'"+email+"\'")

      #Store it in data
      data=cursor.fetchall()

      #Compare user entered password and password in database
      #data[0][0] is used because password is of the form (("***"),)
      if password==data[0][0]:
        
        #If passwords match allow user to enter home-page
        request.session['email']=email
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
      cursor.execute("select count(*) from friends_login_detail where email=\'"+email+"\'")
      data=cursor.fetchall()
      
      if data[0][0]==1:
        #If exists, send error
        return render(request,"error.html")
      
      else:
        #If does not exist, add new details into database
        cursor.execute("insert into friends_login_detail values(\'"+email+"\',\'"+password+"\',\'"+name+"\')")
        cursor.execute("insert into friends_hobbies values(\'"+email+"\',\'\');")
        #Show user that signup has been completed
        return render(request,"success.html")
    except:
      return render(request,"error.html")
    
  #GET request   
  return render(request, "signup.html")

def home(request):
  #POST request
  if request.method == 'POST':
    hobbies=request.POST['hobbies'].split(',')
    email=request.session.get('email')
    
    #MySQL cursor initialization
    cursor=connection.cursor()

    try:
      cursor.execute("select * from friends_hobbies;")
      data=cursor.fetchall()
      final_lis=[]
      lis=[]
      for record in data:
        cursor.execute("select user_name from friends_login_detail where email =\'"+record[0]+"\'")
        name=cursor.fetchall()
        lis.append([name[0][0],record[0]])
        lis.append(record[1].split(','))
        final_lis.append(lis)
        lis=[]
      hobbies_set=set(hobbies)
      sorted_final_lis=sorted(final_lis,key=lambda x:len(hobbies_set.intersection(x[1])))[::-1]
      for i in range(len(sorted_final_lis)):
        if(len(hobbies_set.intersection(sorted_final_lis[i][1]))==0):
          del sorted_final_lis[i]
      sorted_final_lis=[sorted_final_lis[i*4:(i+1)*4] for i in range((len(sorted_final_lis)+4-1)//4)]
      return render(request,"matches.html",{"friends":sorted_final_lis})
    except:
      return render(request,"error.html")

  return render(request, "home.html")


def myhobbies(request):
  #POST request
  if request.method == 'POST':
    hobbies=request.POST['hobbies']
    email=request.session.get('email')
    
    #MySQL cursor initialization
    cursor=connection.cursor()

    try:
      cursor.execute("update friends_hobbies set hobbies=\'"+hobbies+"\' where email=\'"+email+"\'")
      return render(request,"home.html")
    except:
      return render(request,"error.html")

  #GET request
  #MySQL cursor initialization
  cursor=connection.cursor()
  email=request.session.get('email')
  try:
    cursor.execute("select hobbies from friends_hobbies where email=\'"+email+"\'")
    data=cursor.fetchall()    
    return render(request, "myhobbies.html",{"hobbies":data[0][0]})
  except:
    return render(request,"error.html")



