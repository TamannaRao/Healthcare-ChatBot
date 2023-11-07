from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth import login as auth_login  # Rename to avoid conflicts
from chatbot import settings
from django.http import JsonResponse
from .models import ChatHistory
import sys


# Create your views here.
def start(request):
   return render(request,"authentication/start.html")

def signin(request):
   if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username,password=password)

    if user is not None:
      auth_login(request, user)
      return redirect('chathome')

    else:
      messages.error(request,"Invalid Credentails!")
      
      


   return render(request,"authentication/signin.html")



def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        
        if User.objects.filter(username=username):
           messages.error(request,"Username already exist ! please try other username !\n")
           return redirect("signup")

           
        if User.objects.filter(email=email):
           messages.error(request,"Email already registered! Please use another Email.")
           return redirect("signup")

        
        if len(username)>15:
           messages.error(request,"Username should be less than or equal to 15 characters ")
           return redirect("signup")

        if password  != confirmPassword :
           messages.error(request,'Passwords do not match !')
           return redirect("signup")
        

        if not username.isalnum():
           messages.error(request,"Username must be Alpha-Numeric")
           return redirect('signup')
        
       

        myuser = User.objects.create_user(username, email, password)
        myuser.save()

        # Automatically log in the user after successful registration
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)

        
        return redirect('chathome')  # Redirect to chathome after signup
    
    return render(request, "authentication/signup.html")



    


def signout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully!")
    return redirect('start')

def chathome(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return redirect('chathistory')       
        return render(request, "authentication/chathome.html")
    else:
       return redirect('start')
    
def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_user = request.user
            current_password = request.POST['current-password']
            new_password = request.POST['new-password']
            confirm_password = request.POST['confirm-password']

            if not request.user.check_password(current_password):
                messages.error(request, "Incorrect current password")
            elif new_password != confirm_password:
                messages.error(request, "Passwords do not match")
            else:
                current_user.set_password(new_password)
                current_user.save()
                messages.success(request, "Password updated successfully")
                return redirect('chathome')
        return render(request, "authentication/profile.html")
    else:
        return redirect('start')



# ... other view functions ...

def chathistory(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Assuming you have a 'message' field in your form
            message_content = request.POST.get('message')
            
            if message_content:
                chat_history = ChatHistory(user=request.user, content=message_content)
                chat_history.save()

        chat_history = ChatHistory.objects.filter(user=request.user)
        return render(request, "authentication/chathistory.html", {'chat_history': chat_history})
    else:
        return redirect('start')
    
def store_message(request):
    if request.method == "POST":
        message_content = request.POST.get("message-content")
        # Save the message in the database
        chat_history = ChatHistory(user=request.user, content=message_content)
        chat_history.save()
        return JsonResponse({"message": "Message stored successfully"})
    return JsonResponse({"error": "Invalid request method"})


def getResponse(request):
   global chatResponse
   userM= request.GET.get('userM')
   if userM=="Ritika" or userM=="ritika":
       chatResponse="Hello Ritika, what symptoms are you experiencing?"
   elif userM=="Tamanna" or userM=="tamanna":
       chatResponse="Hi Tamanna, what symptoms are you experiencing?"
   elif userM=="stomach pain" :
       chatResponse="Okay, for how many days?"
   elif userM=="high" :
       chatResponse="Okay. From how many days ?"
   elif userM=="2" or userM=="4" :
       chatResponse="Are you experiencing any other symptoms like vomitting or acidity?"
   elif userM=="Yes" or userM=="yes" :
       chatResponse="Okay, are you also experiencing chest pain?"
   else :    
       chatResponse="It might not be that bad but you should take precautions.You may have  GERD.Gastroesophageal reflux disease, or GERD, is a digestive disorder that affects the lower esophageal sphincter (LES), the ring of muscle between the esophagus and stomach. Many people, including pregnant women, suffer from heartburn or acid indigestion caused by GERD.Take following measures :1 ) avoid fatty spicy food 2 ) avoid lying down after eating 3 ) maintain healthy weight 4 ) exercise"
   return HttpResponse(chatResponse)
