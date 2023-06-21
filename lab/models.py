from django.db import models
from django.contrib.auth.models import User
from django import forms
class LabRoom(models.Model):
    room_number = models.IntegerField(unique=True)
    room_description=models.CharField(max_length=100000,default='Write here...')


class Reagent(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    alert_quantity=models.DecimalField(max_digits=10, decimal_places=2, default=100)

class LabEquipment(models.Model):
    name = models.CharField(max_length=100)
    lab_room = models.ForeignKey(LabRoom, on_delete=models.CASCADE)


class Reservation(models.Model):
    lab_room = models.ForeignKey(LabRoom, on_delete=models.CASCADE)
    lab_equipment = models.ForeignKey(LabEquipment,on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)





