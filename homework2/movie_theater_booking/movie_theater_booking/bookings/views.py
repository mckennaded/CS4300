import json
import os
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

SEATS_FILE = os.path.join(os.path.dirname(__file__), 'seats.json')
BOOKINGS_FILE = os.path.join(os.path.dirname(__file__), 'bookings.json')
MOVIES_FILE = os.path.join(os.path.dirname(__file__), 'movies.json')

def load_json(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def movie_list(request):
    movies = load_json(MOVIES_FILE)
    return render(request, 'bookings/movie_list.html', {'movies': movies})

@require_http_methods(["GET", "POST"])
def seat_booking(request, movie_id):
    seats = load_json(SEATS_FILE)
    bookings = load_json(BOOKINGS_FILE)

    if request.method == 'POST':
        selected_seat = request.POST.get('seat')
        if selected_seat:
            for seat in seats:
                if seat['seat_number'] == selected_seat:
                    if seat.get('is_booked', False):
                        return render(request, 'bookings/seat_booking.html', {
                            'movie_id': movie_id,
                            'seats': seats,
                            'error': 'Seat already booked!'
                        })
                    seat['is_booked'] = True
                    bookings.append({
                        'movie_id': movie_id,
                        'seat': selected_seat,
                        'user': request.user.username if request.user.is_authenticated else 'Guest',
                        'booking_date': '2025-10-07'
                    })
                    save_json(SEATS_FILE, seats)
                    save_json(BOOKINGS_FILE, bookings)
                    return redirect(reverse('booking_history'))
        else:
            return render(request, 'bookings/seat_booking.html', {
                'movie_id': movie_id,
                'seats': seats,
                'error': 'No seat selected.'
            })

    return render(request, 'bookings/seat_booking.html', {'movie_id': movie_id, 'seats': seats})

def booking_history(request):
    bookings = load_json(BOOKINGS_FILE)
    movies = load_json(MOVIES_FILE)
    username = request.user.username if request.user.is_authenticated else 'Guest'

    # Filter user bookings
    user_bookings = [b for b in bookings if b.get('user') == username]

    # Create a dict for movie id -> title lookups (assuming movie_id = index + 1)
    movie_titles = {index + 1: movie['title'] for index, movie in enumerate(movies)}

    # Annotate bookings with movie title
    for booking in user_bookings:
        movie_id = int(booking.get('movie_id', 0))
        booking['movie_title'] = movie_titles.get(movie_id, 'Unknown')

    return render(request, 'bookings/booking_history.html', {'bookings': user_bookings})