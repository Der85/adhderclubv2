from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('smart/', include('notes.urls')),  # Include the `notes` app URLs
    path('', include('home.urls')),        # Include the `home` app URLs
]
