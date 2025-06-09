from django.urls import path
from . import views

urlpatterns = [
    path('sql-summary/', views.sql_summary_upload, name='sql_summary'),
]
