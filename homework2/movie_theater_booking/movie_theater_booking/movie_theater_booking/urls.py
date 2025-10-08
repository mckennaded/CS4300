from django.contrib import admin
from django.urls import path, include
from bookings.views import movie_list  # Import movie_list directly for root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie_list, name='home'),  # Root URL displays movie list
    path('', include('bookings.urls')),  # Include bookings app URLs (seat booking, history, etc.)
]
