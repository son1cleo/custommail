from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput

class UserRegisterForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username','email','password1','password2']

class Loginform(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class EmailForm(forms.Form):
    mail_title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    task_link = forms.URLField()
    recipients = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipients'].choices = [
            (user.email, f"{user.first_name} {user.last_name}") for user in User.objects.all()
        ]