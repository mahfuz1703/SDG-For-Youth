from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, 'index.html')

def singin(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!!")
        return redirect(home)
    
    if  request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            error_message = "Please provide both username and password."
            return render(request, "authentication/signin.html", {'error_message': error_message})
        elif User.objects.filter(username=username).exists():
            error_message = "User not found!! Provide valid credintials."
            return render(request, "authentication/signin.html", {'error_message': error_message})

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect(reverse('admin:index'))
            else:
                messages.success(request, "You are successfully logged in!!")
                return redirect(home)
        else:
            error_message = "User not found!! Provide valid credintials."
            return render(request, "authentication/signin.html", {'error_message': error_message})
    return render(request, "authentication/signin.html")
