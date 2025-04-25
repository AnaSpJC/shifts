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


@csrf_exempt  # Para permitir solicitudes desde JavaScript
@login_required
def add_reservation(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)  # 👀 Datos enviados desde FullCalendar
        print("Datos recibidos:", data)  # 👀 Verifica qué llega a la vista

        date = data.get("date")  # Verifica si 'date' está bien recibido

        if Reservation.objects.filter(date=date, is_confirmed=True).exists():
            return JsonResponse({"error": "Ese turno ya está reservado"}, status=400)

        reserva = Reservation.objects.create(
            user=request.user,  # Usuario autenticado
            date=date,          # Fecha seleccionada
            time="10:00",       # Hora fija (puedes hacerla dinámica luego)
            is_confirmed=False  # Reserva inicialmente pendiente
        )
        print("Reserva creada:", reserva)  # 👀 Verifica si se crea correctamente
        return JsonResponse({"message": "Reserva añadida", "reserva_id": reserva.id})
    
    return JsonResponse({"error": "Método no permitido"}, status=405)



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
