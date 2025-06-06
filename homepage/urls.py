from django.urls import path
from . import views

app_name = "homepage"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Root goes to dashboard
]
