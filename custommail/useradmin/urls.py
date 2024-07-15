from django.urls import path
from . import views
from useradmin import views

urlpatterns = [

    path('',views.home,name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('createMail/',views.createMail, name='create_Mail' )

]