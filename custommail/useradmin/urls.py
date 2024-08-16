from django.urls import path
from . import views
from useradmin import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('signup/', views.signup, name='signup'),
    path('createMail/',views.createMail, name='create_Mail' ),
    path('logout/',views.logout,name='logout'),
    path('success/', views.success_page, name='success_page'),
    path('mail/<int:id>/', views.mail_detail, name='mail_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)