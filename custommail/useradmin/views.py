from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from .forms import UserRegisterForm, Loginform
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# email imports
from django.core.mail import send_mail , EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string # for rendering html template 
from django.core import mail
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


# home/dashboard
@login_required(login_url='login')
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
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('home')
            else:
                messages.error(request, 'Username or password is incorrect')

    
    context = {'form':form}
    return render(request, 'useradmin/login.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect('login')

# create mail

@login_required(login_url='login')
def createMail(request):
    if request.method == 'POST':
        mail_title = request.POST.get('mail-title')
        description = request.POST.get('description')
        task_link = request.POST.get('task-link')
        recipients = request.POST.getlist('recipient')
        
        # Handle file upload
        if 'image-upload' in request.FILES:
            image = request.FILES['image-upload']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)
        else:
            image_url = None

        context = {
            'mail_title': mail_title,
            'description': description,
            'task_link': task_link,
            'image_url': image_url,  # Add image URL to context
            'user': request.user,
        }
        
        html_message = render_to_string('useradmin/emailtemp.html', context)
        plain_message = f'{description}\n\nTask Link: {task_link}'
        from_email = settings.EMAIL_HOST_USER

        email_message = EmailMultiAlternatives(
            mail_title, plain_message, from_email, recipients
        )
        email_message.attach_alternative(html_message, "text/html")
        
        # Attach the image if it exists
        if image_url:
            email_message.attach_file(fs.path(filename))
        
        email_message.send()
        return redirect('success_page')  # Redirect to a success page after sending the email

    users = User.objects.all()
    return render(request, 'useradmin/createMail.html', {'users': users}) # Pass the users to the template

def success_page(request):
    messages.success(request, 'Email sent successfully')
    return render(request, 'useradmin/index.html')