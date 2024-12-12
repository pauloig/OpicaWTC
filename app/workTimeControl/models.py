from contextlib import nullcontext
from operator import truediv
from pyexpat import model
from random import choices
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.core.validators import validate_email
from catalog import models as catalogModel

payment_choice = (
    
    (1, 'Credit/Debit Card'),
    (2, 'Cash'),
)

class paidByTheHour(models.Model):
    date = models.DateField(blank=True, null=True)
    EmployeeID = models.ForeignKey(catalogModel.Employee , on_delete=models.CASCADE, db_column ='EmployeeID', null=False, blank=False)
    clockIn = models.TimeField(null=True, blank=True)
    clockOut = models.TimeField(null=True, blank=True)
    breakIn = models.TimeField(null=True, blank=True)
    breakOut = models.TimeField(null=True, blank=True)
    lunchIn = models.TimeField(null=True, blank=True)
    lunchOut = models.TimeField(null=True, blank=True)
    total_hours = models.FloatField(null=True, blank=True)
    regular_hours = models.FloatField(null=True, blank=True)
    overtime_hours = models.FloatField(null=True, blank=True)
    double_time = models.FloatField(null=True, blank=True)
    vacation_hours = models.FloatField(null=True, blank=True)
    sick_hours = models.FloatField(null=True, blank=True)    
    holiday_hours = models.FloatField(null=True, blank=True)
    other_hours = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return str(self.date) + ' - ' + str(self.EmployeeID)
    
    class Meta:
        unique_together = ('date','EmployeeID')


class paidByComission(models.Model):
    EmployeeID = models.ForeignKey(catalogModel.Employee , on_delete=models.CASCADE, db_column ='EmployeeID', null=False, blank=False)
    ClientID = models.ForeignKey(catalogModel.Client , on_delete=models.CASCADE, db_column ='ClientID', null=False, blank=False)
    service_date = models.DateField(blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    payment_number = models.IntegerField(blank=True, null=True)
    payment_method = models.IntegerField(default=1, choices = payment_choice)
    payment_card = models.CharField(max_length=60, blank=True, null=True)
    payment_amount = models.FloatField(null=True, blank=True)
    rate = models.IntegerField()
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return str(self.service_date) + ' - ' + str(self.EmployeeID) + ' - ' + str(self.ClientID)
    

class paidBySalary(models.Model):
    EmployeeID = models.ForeignKey(catalogModel.Employee , on_delete=models.CASCADE, db_column ='EmployeeID', null=False, blank=False)
    periodID = models.ForeignKey(catalogModel.period , on_delete=models.CASCADE, db_column ='PeriodID', null=False, blank=False)
    date = models.DateField(blank=True, null=True)
    regular_hours = models.FloatField(null=True, blank=True)
    vacation_hours = models.FloatField(null=True, blank=True)
    sick_hours = models.FloatField(null=True, blank=True)
    other_hours = models.FloatField(null=True, blank=True)
    holiday_hours = models.FloatField(null=True, blank=True)
    status = models.IntegerField(choices = catalogModel.period_status_choice)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return str(self.EmployeeID) + ' - ' + str(self.periodID) + ' - ' + str(self.date)
    
    class Meta:
        unique_together = ('date','EmployeeID')

    