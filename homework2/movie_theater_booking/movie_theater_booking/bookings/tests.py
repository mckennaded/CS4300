from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import json
import os

SEATS_FILE = os.path.join(os.path.dirname(__file__), 'seats.json')
BOOKINGS_FILE = os.path.join(os.path.dirname(__file__), 'bookings.json')
MOVIES_FILE = os.path.join(os.path.dirname(__file__), 'movies.json')

def reset_test_files():
    with open(SEATS_FILE, 'w') as f:
        json.dump({
            "1": [
                {"seat_number": "A1", "is_booked": False},
                {"seat_number": "A2", "is_booked": False}
            ],
            "2": [
                {"seat_number": "A1", "is_booked": False},
                {"seat_number": "A2", "is_booked": False}
            ]
        }, f)
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump([], f)
    with open(MOVIES_FILE, 'w') as f:
        json.dump([
            {"title": "Movie 1", "description": "Desc 1", "release_date": "2024-01-01", "duration": 120},
            {"title": "Movie 2", "description": "Desc 2", "release_date": "2024-01-02", "duration": 130}
        ], f)

class BookingAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        reset_test_files()

    def test_movie_list_view(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Movie 1")
        self.assertContains(response, "Movie 2")

    def test_seat_booking_get(self):
        response = self.client.get(reverse('seat_booking', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A1")
        self.assertContains(response, "A2")

    def test_seat_booking_post_success(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('seat_booking', args=[1]), {'seat': 'A1'})
        self.assertEqual(response.status_code, 302)  # Redirect on booking success

        with open(SEATS_FILE) as f:
            seats_data = json.load(f)
            self.assertTrue(seats_data['1'][0]['is_booked'])

        with open(BOOKINGS_FILE) as f:
            bookings = json.load(f)
            self.assertEqual(len(bookings), 1)
            self.assertEqual(bookings[0]['seat'], 'A1')
            self.assertEqual(bookings[0]['user'], 'testuser')

    def test_seat_booking_post_double_booking(self):
        self.client.login(username='testuser', password='testpass')
        self.client.post(reverse('seat_booking', args=[1]), {'seat': 'A1'})  # First booking success
        response = self.client.post(reverse('seat_booking', args=[1]), {'seat': 'A1'})  # Double booking attempt
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seat already booked!")

    def test_booking_history_view(self):
        self.client.login(username='testuser', password='testpass')
        self.client.post(reverse('seat_booking', args=[1]), {'seat': 'A1'})
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Movie 1")
        self.assertContains(response, "A1")
