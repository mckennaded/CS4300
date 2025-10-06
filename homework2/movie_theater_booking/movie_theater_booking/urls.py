from django.urls import path, include

urlpatterns = [
    # Other URLs
    path('', include('bookings.urls')),
]
