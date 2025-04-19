from django.contrib import admin  # type: ignore
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "time", "is_confirmed")  # Muestra estos campos en la vista de admin
    list_filter = ("date", "is_confirmed")  # Permite filtrar reservas por fecha y estado
    search_fields = ("user__username", "date")  # Permite buscar reservas por usuario y fecha
