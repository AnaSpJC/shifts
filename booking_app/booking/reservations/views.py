from django.shortcuts import render, get_object_or_404  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from .models import Reservation
from django.http import JsonResponse

@login_required
def reservations_list(request):
    reservas = Reservation.objects.filter(user=request.user).order_by("date", "time")
    return render(request, "reservations/list.html", {"reservas": reservas})


@login_required
def add_reservation(request):
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")

        if Reservation.objects.filter(date=date, time=time, is_confirmed=True).exists():
            return JsonResponse({"error": "Ese turno ya está reservado"}, status=400)

        reserva = Reservation.objects.create(user=request.user, date=date, time=time, is_confirmed=False)
        return JsonResponse({"message": "Reserva añadida", "reserva_id": reserva.id})


@login_required
def confirm_reservation(request, reserva_id):
    reserva = get_object_or_404(Reservation, id=reserva_id, user=request.user)
    reserva.is_confirmed = True
    reserva.save()
    return JsonResponse({"message": "Reserva confirmada"})



def reservations_events(request):
    reservas = Reservation.objects.filter(is_confirmed=True)  # Solo turnos confirmados
    events = [
        {"title": f"Reservado", "start": str(reserva.date) + "T" + str(reserva.time)}
        for reserva in reservas
    ]
    return JsonResponse(events, safe=False)
