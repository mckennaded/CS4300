from django.urls import path
from .views import movie_list, seat_booking, booking_history

urlpatterns = [
    path('movies/', movie_list, name='movie_list'),
    path('movies/<int:movie_id>/seats/', seat_booking, name='seat_booking'),
    path('bookings/history/', booking_history, name='booking_history'),
    path('', include('bookings.urls')),
]

