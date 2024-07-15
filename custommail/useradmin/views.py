from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from django.contrib import messages
from .forms import UserRegisterForm,Loginform
from django.contrib.auth import authenticate

# Create your views here.
def home (request):
    return render(request,'useradmin/index.html')
# register

def signup(request):
    form = UserRegisterForm()
    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created successfully')
            return redirect('login')
            #return redirect('')

    context = {'form':form}

    return render(request, 'useradmin/signup.html', context=context)

# login
def login(request):
    form = Loginform()

    if request.method == 'POST':
        form = Loginform(request, data = request.POST)
        if form.is_valid():
            username = request.POST('username')
            password = request.POST('password')
            
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or password is incorrect')

    
    context = {'form':form}
    return render(request, 'useradmin/login.html', context=context)

def createMail(request):
    return render(request,'useradmin/createMail.html')