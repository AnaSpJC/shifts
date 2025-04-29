from django.urls import path
from .views import reservations_list, add_reservation, confirm_reservation, reservations_events, available_time_slots, reservations_list_json

urlpatterns = [
    path("mis-reservas/", reservations_list, name="reservations_list"),
    path("agregar/", add_reservation, name="add_reservation"),
    path("confirmar/<int:reserva_id>/", confirm_reservation, name="confirm_reservation"),
    path("eventos/", reservations_events, name="reservations_events"),
    path("horarios-disponibles/", available_time_slots, name="available_time_slots"),
    path("mis-reservas-json/", reservations_list_json, name="reservations_list_json"),
]