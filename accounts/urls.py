from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('otp_verify/', views.otp_verify, name='otp_verify'),
    path('login/', views.login_view, name='login'),
    path('login_otp/', views.login_otp, name='login_otp'),
    path('logout/', views.logout_view, name='logout'),
]
