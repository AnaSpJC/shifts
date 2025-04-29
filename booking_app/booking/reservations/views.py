from django.shortcuts import render, get_object_or_404 
from django.contrib.auth.decorators import login_required  
from .models import Reservation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def reservations_list(request):
    print("Usuario autenticado:", request.user)
    reservas = Reservation.objects.filter(user=request.user).order_by("date", "time")
    return render(request, "reservations/list.html", {"reservas": reservas})


@login_required
def add_reservation(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)  # Datos enviados desde FullCalendar
        print("Datos recibidos:", data)  # Verifica qué llega a la vista

        date = data.get("date")  # Fecha enviada
        time = data.get("time")  # Horario enviado

        # Validar si ya existe una reserva confirmada en la misma fecha y horario
        if Reservation.objects.filter(date=date, time=time, is_confirmed=True).exists():
            return JsonResponse({"error": "Ese horario ya está reservado"}, status=400)

        # Crear la nueva reserva
        reserva = Reservation.objects.create(
            user=request.user,
            date=date,
            time=time,
            is_confirmed=False  # Reserva inicialmente pendiente
        )
        print("Reserva creada:", reserva)  # Confirma en la consola
        return JsonResponse({"message": "Reserva añadida", "reserva_id": reserva.id})
    
    return JsonResponse({"error": "Método no permitido"}, status=405)


@login_required
def confirm_reservation(request, reserva_id):
    reserva = get_object_or_404(Reservation, id=reserva_id, user=request.user)
    if request.method == "POST":
        reserva.is_confirmed = True
        reserva.save()
        return JsonResponse({"message": "Reserva confirmada"})
    return JsonResponse({"error": "Método no permitido"}, status=405)



def reservations_events(request):
    reservas = Reservation.objects.filter(is_confirmed=True)  # Solo turnos confirmados
    events = [
        {"title": f"Reservado", "start": f"{reserva.date}T{reserva.time}"}
        for reserva in reservas
    ]
    return JsonResponse(events, safe=False)

@login_required
def available_time_slots(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)

        date = data.get("date")

        # Horarios disponibles
        AVAILABLE_TIME_SLOTS = [
            "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"
        ]

        # Reservas existentes para esa fecha
        reserved_slots = Reservation.objects.filter(date=date).values_list("time", flat=True)

        # Filtrar horarios disponibles
        available_slots = [slot for slot in AVAILABLE_TIME_SLOTS if slot not in reserved_slots]

        return JsonResponse(available_slots, safe=False)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def reservations_list_json(request):
    reservas = Reservation.objects.filter(user=request.user).order_by("date", "time")
    reservas_json = [
        {"id": reserva.id, "date": str(reserva.date), "time": str(reserva.time), "is_confirmed": reserva.is_confirmed}
        for reserva in reservas
    ]
    return JsonResponse(reservas_json, safe=False)


