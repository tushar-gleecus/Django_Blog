from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login_view(request):
    return render(request, "accounts/login.html")  # Use full path if needed

def register(request):
    return render(request, "accounts/register.html")  # Use full path if needed

@login_required
def dashboard(request):
    cards = [
        {"title": "SQL Summary", "description": "Summarize your SQL data quickly.", "link": "#"},
        {"title": "Sync Data to GCP", "description": "Seamlessly synchronize data to Google Cloud.", "link": "#"},
        {"title": "Data Visualization", "description": "Generate rich charts and reports.", "link": "#"},
        {"title": "User Management", "description": "Add or manage users and permissions.", "link": "#"},
        {"title": "Notifications", "description": "Set up and view alerts.", "link": "#"},
        {"title": "Settings", "description": "Configure application preferences.", "link": "#"},
    ]
    return render(request, 'homepage/index.html', {'cards': cards})

# You can rename 'dashboard' to 'index' or whatever suits your url mapping.
