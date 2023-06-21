from django.contrib import admin
from .models import LabRoom, Reagent, Reservation, LabEquipment


class LabRoomAdmin(admin.ModelAdmin):
    list_display = ['room_number','room_description']
    # Add any other customizations you want

class ReagentAdmin(admin.ModelAdmin):
    list_display = ['name']
    # Add any other customizations you want

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'lab_room', 'lab_equipment', 'start_time', 'end_time']

class LabEquipmentAdmin(admin.ModelAdmin):
    list_display = ['name','lab_room']

admin.site.register(LabRoom, LabRoomAdmin)
admin.site.register(Reagent, ReagentAdmin )
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(LabEquipment, LabEquipmentAdmin)
