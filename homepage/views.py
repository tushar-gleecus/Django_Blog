from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    cards = [
        {"title": "SQL Summary", "description": "Summarize your SQL data quickly.", "link": "#"},
        {"title": "Sync Data to GCP", "description": "Seamlessly synchronize data to Google Cloud.", "link": "#"},
        {"title": "Data Visualization", "description": "Generate rich charts and reports.", "link": "#"},
        {"title": "User Management", "description": "Add or manage users and permissions.", "link": "#"},
        {"title": "Notifications", "description": "Set up and view alerts.", "link": "#"},
        {"title": "Settings", "description": "Configure application preferences.", "link": "#"},
    ]
    return render(request, 'homepage/index.html', {'cards': cards})
