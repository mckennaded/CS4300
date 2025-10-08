import json
import os
from django.shortcuts import render

def movie_list(request):
    file_path = os.path.join(os.path.dirname(__file__), 'movies.json')
    with open(file_path, 'r') as f:
        movies = json.load(f)
    return render(request, 'bookings/movie_list.html', {'movies': movies})

def seat_booking(request, movie_id):
    # Logic to display seats for movie_id, read from JSON or in-memory data
    seats = [
        {"seat_number": "A1", "is_booked": False},
        {"seat_number": "A2", "is_booked": True},
        {"seat_number": "A3", "is_booked": False},
    ]
    return render(request, 'bookings/seat_booking.html', {'movie_id': movie_id, 'seats': seats})

def booking_history(request):
    # Logic to fetch booking history from file/session/database as suits your setup
    bookings = [
        {"movie_title": "Luca", "seat": "A1", "booking_date": "2025-10-01"},
        {"movie_title": "Encanto", "seat": "B3", "booking_date": "2025-10-05"},
    ]
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})
