from django.shortcuts import render, redirect
from .models import LabRoom, Reagent, Reservation, LabEquipment
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import HttpResponseBadRequest




from django.shortcuts import render, redirect
from .models import Reservation

@login_required
def my_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)

    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        reservation = Reservation.objects.get(id=reservation_id)


        if reservation.user == user:
            reservation.delete()
            return redirect('my_reservations')

    context = {
        'reservations': reservations
    }
    return render(request, 'my_reservations.html', context)

def delete_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)




    reservation.delete()


    return redirect('my_reservations')


def home(request):
    return render(request, 'home.html')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def book_lab(request):
    lab_rooms = LabRoom.objects.all()
    lab_equipment=LabEquipment.objects.all()
    reservations = Reservation.objects.all()
    context = {
        'lab_rooms': lab_rooms,
        'lab_equipment': lab_equipment,
        'reservations': reservations
    }
    return render(request, 'book_lab.html', context)
@login_required
def reagents(request):
    reagents = Reagent.objects.all()
    return render(request, 'reagents.html', {'reagents': reagents})

@login_required
def lab_equipment(request):
    lab_equipment = LabEquipment.objects.all()
    return render(request, 'lab_equipment.html', {'lab_equipment': lab_equipment})

@login_required
def used_reagents(request):
    if request.method == 'POST':
        for reagent_id, quantity in request.POST.items():
            if reagent_id != 'csrfmiddlewaretoken':
                reagent = Reagent.objects.get(id=reagent_id)
                if quantity.strip() != '':
                    reagent.quantity -= int(quantity)
                reagent.save()
        return redirect('home')
    else:
        reagents = Reagent.objects.all()
        return render(request, 'used_reagents.html', {'reagents': reagents})
@login_required
def lab_rooms_view(request):

    lab_rooms = LabRoom.objects.all()


    context = {'lab_rooms': lab_rooms}


    return render(request, 'lab_rooms.html', context)
@login_required
def add_reservation(request):
    if request.method == 'POST':
        lab_room_id = request.POST.get('lab_room')
        lab_equipment_id = request.POST.get('lab_equipment')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        user = request.user

        lab_room = LabRoom.objects.get(id=lab_room_id)
        lab_equipment = LabEquipment.objects.get(id=lab_equipment_id)

        reservation = Reservation(
            lab_room=lab_room,
            lab_equipment=lab_equipment,
            start_time=start_time,
            end_time=end_time,
            user=user
        )
        reservation.save()

        #messages.success(request, 'Reservation added successfully.')
        return redirect('book_lab')

    return redirect('book_lab')









from django.http import JsonResponse
from .models import Reservation

def get_availability(request):
    lab_room_id = request.GET.get('lab_room_id')

    availability = Reservation.objects.filter(lab_room_id=lab_room_id)


    response = [{'start_time': reservation.start_time, 'end_time': reservation.end_time} for reservation in availability]
    return JsonResponse(response, safe=False)
import json
@login_required
# def get_reservations(request):
#     if request.method == 'GET' and 'lab_room_id' in request.GET:
#         lab_room_id = request.GET.get('lab_room_id')
#         lab_room = LabRoom.objects.get(id=lab_room_id)
#         reservations = Reservation.objects.filter(lab_room=lab_room)
#
#         reservation_data = []
#         for reservation in reservations:
#             reservation_data.append({
#                 'title': 'Reserved',
#                 'start': reservation.start_time.strftime('%Y-%m-%d %H:%M:%S'),
#                 'end': reservation.end_time.strftime('%Y-%m-%d %H:%M:%S'),
#                 'color': 'red'
#             })
#
#         return HttpResponse(json.dumps(reservation_data), content_type='application/json')
#
#     return HttpResponseBadRequest('Invalid request')

# def get_reservations(request):
#     if request.method == 'GET' and 'lab_room_id' in request.GET and 'lab_equipment_id' in request.GET:
#         lab_room_id = request.GET.get('lab_room_id')
#         lab_equipment_id = request.GET.get('lab_equipment_id')
#
#         lab_room = LabRoom.objects.get(id=lab_room_id)
#         lab_equipment = LabEquipment.objects.get(id=lab_equipment_id)
#
#         reservations = Reservation.objects.filter(lab_room=lab_room, lab_equipment=lab_equipment)
#
#         reservation_data = []
#         for reservation in reservations:
#             reservation_data.append({
#                 'title': 'Reserved',
#                 'start': reservation.start_time.strftime('%Y-%m-%d %H:%M:%S'),
#                 'end': reservation.end_time.strftime('%Y-%m-%d %H:%M:%S'),
#                 'color': 'red'
#             })
#
#         return HttpResponse(json.dumps(reservation_data), content_type='application/json')
#
#     return HttpResponseBadRequest('Invalid request')

def get_reservations(request):
    if request.method == 'GET' and 'lab_room_id' in request.GET:
        lab_room_id = request.GET.get('lab_room_id')
        lab_equipment_id = request.GET.get('lab_equipment_id')

        lab_room = LabRoom.objects.get(id=lab_room_id)

        if lab_equipment_id:
            lab_equipment = LabEquipment.objects.get(id=lab_equipment_id)
            reservations = Reservation.objects.filter(lab_room=lab_room, lab_equipment=lab_equipment)
        else:
            reservations = Reservation.objects.filter(lab_room=lab_room)

        reservation_data = []
        for reservation in reservations:
            reservation_data.append({
                'title': 'Reserved',
                'start': reservation.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end': reservation.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'color': 'red'
            })

        return HttpResponse(json.dumps(reservation_data), content_type='application/json')

    return HttpResponseBadRequest('Invalid request')

from django.http import JsonResponse

def get_lab_equipments(request):
    if request.method == 'GET' and 'lab_room_id' in request.GET:
        lab_room_id = request.GET.get('lab_room_id')
        lab_equipments = LabEquipment.objects.filter(lab_room_id=lab_room_id)
        data = [{'id': equipment.id, 'name': equipment.name} for equipment in lab_equipments]
        return JsonResponse(data, safe=False)
    return JsonResponse({}, status=400)