from django.urls import path
from . import views
from .views import logout_view
from .views import get_availability

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('book_lab/', views.book_lab, name='book_lab'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('add_reservation/', views.add_reservation, name='add_reservation'),
    path('register/', views.register, name='register'),
    path('reagents/', views.reagents, name='reagents'),
    path('logout/', logout_view, name='logout'),
    path('lab_rooms/', views.lab_rooms_view, name='lab_rooms'),
    path('get_availability/', views.get_availability, name='get_availability'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('get_reservations/', views.get_reservations, name='get_reservations'),
]




