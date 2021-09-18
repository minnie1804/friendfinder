from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection

#base.html is a default template used to display messages to user
#we have used \' in mysql cursor statements to display a nested quote symbol within ""

def login(request):

  #If user is alreaddy logged in, it will logout
  if (request.session.has_key("email")):
    del request.session["email"]

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
        #If passwords dont match, show error message
        return render(request,"base.html",{"msg":"Oops, we ran into an error"})
      
    except:
      return render(request,"base.html",{"msg":"Oops, we ran into an error"})
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
        return render(request,"base.html",{"msg":"Oops, we ran into an error"})
      
      else:
        #If does not exist, add new details into database
        cursor.execute("insert into friends_login_detail values(\'"+email+"\',\'"+password+"\',\'"+name+"\')")
        cursor.execute("insert into friends_hobbies values(\'"+email+"\',\'\');")

        #Show user that signup has been completed
        return render(request,"base.html",{"msg":"Sign-up success"})
    except:
      return render(request,"base.html",{"msg":"Oops, we ran into an error"})
    
  #GET request   
  return render(request, "signup.html")

def home(request):
  #If user is not logged in, it will send them back to login page
  if (not request.session.has_key("email")):
    return redirect("../login")

  #POST request
  if request.method == 'POST':
    #Get the hobbies entered by the user
    hobbies=request.POST['hobbies'].split(',')
    email=request.session.get('email')
    
    #MySQL cursor initialization
    cursor=connection.cursor()

    try:
      #Select hobbies of everyone in database except current user
      cursor.execute("select * from friends_hobbies where email <> \'"+email+"\';")
      data=cursor.fetchall()

      #lis represents each induvidual person holding data of the form [[[Username],[Email]],List of Hobbies]
      #final_list holds all persons
      final_list=[]
      lis=[]

      for record in data:
        #Select username corresponding to email-id from login_details table
        cursor.execute("select user_name from friends_login_detail where email =\'"+record[0]+"\'")
        name=cursor.fetchall()

        #Create lis element
        lis.append([name[0][0],record[0]])
        lis.append(record[1].split(','))

        #append the element to final_list
        final_list.append(lis)

        #Reset the element
        lis=[]

      #Convert hobbies entered in search bar to a set, to use set functions
      hobbies_set=set(hobbies)

      #Sort the final_list based on number of common hobbies in descending order with a custom sort function
      sorted_final_list=sorted(final_list,key=lambda x:len(hobbies_set.intersection(x[1])))[::-1]
      
      #Remove persons who have no hobbies in common
      for i in range(len(sorted_final_list)-1,-1,-1):
        if(len(hobbies_set.intersection(sorted_final_list[i][1]))==0):
          del sorted_final_list[i]
        

      #If no matches found, display message
      if (len(sorted_final_list)==0):
        return render(request,"base.html",{"msg":"Sorry, no matches found"})
      
      #Group the matched persons in groups of 4 to display in html. (So that box doesnt go out of page, it adds a new line)
      sorted_final_list=[sorted_final_list[i*4:(i+1)*4] for i in range((len(sorted_final_list)+4-1)//4)]

      return render(request,"matches.html",{"friends":sorted_final_list})
    except:
      return render(request,"base.html",{"msg":"Oops, we ran into an error"})

  #GET Request
  return render(request, "home.html")


def myhobbies(request):
  #POST request
  if request.method == 'POST':
    hobbies=request.POST['hobbies']
    email=request.session.get('email')
    
    #MySQL cursor initialization
    cursor=connection.cursor()

    try:
      #Update the hobbies of current user
      cursor.execute("update friends_hobbies set hobbies=\'"+hobbies+"\' where email=\'"+email+"\'")
      return render(request,"home.html")
    except:
      return render(request,"base.html",{"msg":"Oops, we ran into an error"})

  #GET request
  #MySQL cursor initialization
  cursor=connection.cursor()
  email=request.session.get('email')
  try:
    #Retrieve hobbies of current user and display
    cursor.execute("select hobbies from friends_hobbies where email=\'"+email+"\'")
    data=cursor.fetchall()  

    return render(request, "myhobbies.html",{"hobbies":data[0][0]})
  except:
    return render(request,"base.html",{"msg":"Oops, we ran into an error"})



