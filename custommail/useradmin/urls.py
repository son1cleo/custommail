from django.urls import path
from . import views
from useradmin import views

urlpatterns = [

    path('',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('signup/', views.signup, name='signup'),
    path('createMail/',views.createMail, name='create_Mail' ),
    path('logout/',views.logout,name='logout'),
    path('success/', views.success_page, name='success_page'),
    

]