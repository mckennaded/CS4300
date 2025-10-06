from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAdminUser]  # Admins can manage movies

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticated]  # Authenticated users can view/book seats

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only view their own bookings
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assign the booking to the logged-in user
        serializer.save(user=self.request.user)

