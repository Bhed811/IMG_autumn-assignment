from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # This includes allauth's URLs
    path('', include('review_system.urls')),  
]

