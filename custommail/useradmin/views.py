from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from .forms import UserRegisterForm, Loginform
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# email imports
from django.core.mail import send_mail , EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string # for rendering html template 
#from django.core import mail
#from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .models import MailHistory, MailImage # for mail history to be shown

from django.shortcuts import render, get_object_or_404
#from .models import Mail  # Replace with your actual model name


# home/dashboard
'''
@login_required(login_url='login')
def home (request):
    return render(request,'useradmin/index.html')
'''

@login_required(login_url='login')
def home(request):
    mail_history = MailHistory.objects.all().order_by('-timestamp')
    print(mail_history)  # Debug print
    return render(request, 'useradmin/index.html', {'mail_history': mail_history})


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

        # Save the mail history
        mail = MailHistory.objects.create(
            title=mail_title,
            description=description,
            task_link=task_link,
            sender=request.user,
            recipients=','.join(recipients)
        )
        
        # Handle file upload
        if 'image-upload' in request.FILES:
            image = request.FILES['image-upload']
            MailImage.objects.create(mail=mail, image=image)

            '''
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)
        else:
            image_url = None
            '''

        context = {
            'description': description,
            'task_link': task_link,
            #'image_url': image_url,  # Add image URL to context
            'image_url': mail.images.first().image.url if mail.images.exists() else None,
            'user' : request.user
        }
        
        html_message = render_to_string('useradmin/emailtemp.html', context)
        plain_message = f'{description}\n\nTask Link: {task_link}'
        from_email = settings.EMAIL_HOST_USER

        email_message = EmailMultiAlternatives(
            mail_title, plain_message, from_email, recipients
        )
        email_message.attach_alternative(html_message, "text/html")
        
        # Attach the image if it exists
        '''if image_url:
            email_message.attach_file(fs.path(filename))
        '''
        if mail.images.exists():
            email_message.attach_file(mail.images.first().image.path)
            
        email_message.send()

        return redirect('success_page')  # Redirect to a success page after sending the email
        #Tried returning to the home page, but for some reason, it was sending duplicate emails.
        #So the success_page body was changed to home body. This stopped the duplicacy.
        
    users = User.objects.all()
    return render(request, 'useradmin/createMail.html', {'users': users})

def success_page(request):
    mail_history = MailHistory.objects.all().order_by('-timestamp')
    print(mail_history)  # Debug print
    return render(request, 'useradmin/index.html', {'mail_history': mail_history})
'''
    messages.success(request, 'Email sent successfully')
    return render(request, 'useradmin/index.html')

    
def index(request):
    mail_history = MailHistory.objects.all().order_by('-timestamp')
    print(mail_history)
    return render(request, 'useradmin/index.html', {'mail_history': mail_history})
'''

# mail history
def mail_detail(request, id):
    mail = get_object_or_404(MailHistory, id=id)
    print(mail.title , mail.sender, mail.recipients, mail.timestamp, mail.description, mail.images, mail.task_link)  # Debugging line
    context = {
        'mail': mail,
    }
    return render(request, 'useradmin/mail_detail.html', {'mail': mail})
