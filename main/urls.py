from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin
from main import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="sign_in"),
    path('register/', views.register, name="sign_up"),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('password_reset/', views.password_reset_request, name="password_reset"),
]


if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
