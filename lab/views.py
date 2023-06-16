from django.shortcuts import render, redirect
from .models import LabRoom, Reagent, Reservation
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import HttpResponseBadRequest



#@login_required
# def my_reservations(request):
#     user = request.user
#     reservations = Reservation.objects.filter(user=request.user)
#     context = {
#         'reservations': reservations
#     }
#     return render(request, 'my_reservations.html', context)
from django.shortcuts import render, redirect
from .models import Reservation

@login_required
def my_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user)

    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        reservation = Reservation.objects.get(id=reservation_id)

        # Check if the reservation belongs to the current user
        if reservation.user == user:
            reservation.delete()
            return redirect('my_reservations')

    context = {
        'reservations': reservations
    }
    return render(request, 'my_reservations.html', context)

def delete_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    # if request.method == 'POST':
    #     reservation.delete()
    #     return redirect('my_reservations')
    # else:
    #     return redirect('my_reservations')
    reagent = reservation.reagent

    # Update the reagent's quantity
    reagent.quantity += reservation.quantity
    reagent.save()

    # Delete the reservation
    reservation.delete()

    # Redirect to the reservations page or any other desired page
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

def book_lab(request):
    lab_rooms = LabRoom.objects.all()
    reagents = Reagent.objects.filter(quantity__gt=0)
    reservations = Reservation.objects.all()
    context = {
        'lab_rooms': lab_rooms,
        'reagents': reagents,
        'reservations': reservations
    }
    return render(request, 'book_lab.html', context)

def reagents(request):
    reagents = Reagent.objects.all()
    return render(request, 'reagents.html', {'reagents': reagents})


def lab_rooms_view(request):
    # Retrieve the lab rooms from the database
    lab_rooms = LabRoom.objects.all()

    # Pass the lab rooms data to the template
    context = {'lab_rooms': lab_rooms}

    # Render the lab rooms template with the provided data
    return render(request, 'lab_rooms.html', context)
@login_required
def add_reservation(request):
    if request.method == 'POST':
        lab_room_id = request.POST.get('lab_room')
        reagent_id = request.POST.get('reagent')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        user = request.user
        quantity = request.POST.get('quantity')

        lab_room = LabRoom.objects.get(id=lab_room_id)
        reagent = Reagent.objects.get(id=reagent_id)

        # Check if the requested quantity is available
        if Decimal(quantity) <= reagent.quantity:
            reservation = Reservation(
                lab_room=lab_room,
                reagent=reagent,
                start_time=start_time,
                end_time=end_time,
                user=user,
                quantity=quantity
            )
            reservation.save()

            # Update the reagent quantity
            reagent.quantity -= Decimal(quantity)
            reagent.save()

            return redirect('book_lab')
        else:
            error_message = "Requested quantity not available"
            # You can handle this error message in the template
            # or pass it in the context to display it to the user

    return redirect('book_lab')

# @login_required
# def add_reservation(request):
#     if request.method == 'POST':
#         lab_room_id = request.POST.get('lab_room')
#         start_time = request.POST.get('start_time')
#         end_time = request.POST.get('end_time')
#         user = request.user
#
#         # Get the list of selected reagents and quantities
#         reagents = request.POST.getlist('reagents')
#         quantities = request.POST.getlist('quantity')
#
#         # Check if the number of reagents and quantities match
#         if len(reagents) != len(quantities):
#             error_message = "Invalid form data: reagents and quantities don't match"
#             return render(request, 'error.html', {'error_message': error_message})
#
#         lab_room = LabRoom.objects.get(id=lab_room_id)
#
#         # Iterate over the reagents and quantities
#         for reagent_id, quantity in zip(reagents, quantities):
#             reagent = Reagent.objects.get(id=reagent_id)
#
#             # Check if the requested quantity is available
#             if Decimal(quantity) <= reagent.quantity:
#                 reservation = Reservation(
#                     lab_room=lab_room,
#                     reagent=reagent,
#                     start_time=start_time,
#                     end_time=end_time,
#                     user=user,
#                     quantity=quantity
#                 )
#                 reservation.save()
#
#                 # Update the reagent quantity
#                 reagent.quantity -= Decimal(quantity)
#                 reagent.save()
#
#             else:
#                 error_message = f"Requested quantity for reagent {reagent.name} not available"
#                 # You can handle this error message in the template
#                 # or pass it in the context to display it to the user
#
#         return redirect('book_lab')
#
#     return redirect('book_lab')


from django.http import JsonResponse

# def get_availability(request):
#     if request.method == 'GET':
#         lab_room_id = request.GET.get('lab_room_id')
#
#         # Fetch availability based on the lab room ID
#         # Add your logic here to retrieve the availability for the selected lab room
#         availability = ...
#
#         # Prepare the availability data
#         availability_data = []
#         for item in availability:
#             availability_data.append({
#                 'start_time': item.start_time.strftime('%Y-%m-%d %H:%M:%S'),
#                 'end_time': item.end_time.strftime('%Y-%m-%d %H:%M:%S')
#             })
#
#         return JsonResponse(availability_data, safe=False)

from django.http import JsonResponse


from django.http import JsonResponse
from .models import Reservation

def get_availability(request):
    lab_room_id = request.GET.get('lab_room_id')
    # Implement your logic to fetch availability data based on lab_room_id
    availability = Reservation.objects.filter(lab_room_id=lab_room_id)

    # Convert the availability data to a JSON response
    response = [{'start_time': reservation.start_time, 'end_time': reservation.end_time} for reservation in availability]
    return JsonResponse(response, safe=False)
import json
@login_required
def get_reservations(request):
    if request.method == 'GET' and 'lab_room_id' in request.GET:
        lab_room_id = request.GET.get('lab_room_id')
        lab_room = LabRoom.objects.get(id=lab_room_id)
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