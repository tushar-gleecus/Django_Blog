from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls', namespace='homepage')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('sql-summary/', include('sqltools.urls')),

]
