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

gender_choice = (
    ('M', 'Male'),
    ('F', 'Female'),
)

period_status_choice = (
    (1, 'Open'),
    (2, 'supervisor approved'),
    (3, 'Closed'),
)

class Department(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)


    def __str__(self):
        return self.name
    

class JobTitle(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)


    def __str__(self):
        return self.name

class Code(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)


    def __str__(self):
        return self.name    

class EmpType(models.Model):
    empTypeID = models.IntegerField(primary_key=True, serialize=False)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)


    def __str__(self):
        return  self.name  
    
class EmptStatus(models.Model):
    empStatusID = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)


    def __str__(self):
        return  self.name  
    


class Employee(models.Model):
    employeeID = models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address_city = models.CharField(max_length=100, blank=True, null= True)
    address_state = models.CharField(max_length=100, blank=True, null= True)
    address_street = models.CharField(max_length=100, blank=True, null= True)
    address_zip = models.CharField(max_length=30, blank=True, null= True)
    phone_number = models.CharField(max_length=30, blank=True, null= True)
    gender = models.CharField(max_length=2, choices = gender_choice)
    Department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    rate = models.IntegerField()
    rate_by_hour = models.IntegerField(null=True, blank=True)
    schedule_by_day = models.FloatField(null=True, blank=True)
    JobTitle = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True)
    EmpType = models.ForeignKey(EmpType, on_delete=models.SET_NULL, null=True, blank=True)
    EmptStatus = models.ForeignKey(EmptStatus, on_delete=models.SET_NULL, null=True, blank=True)
    birthDate = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null= True, validators=[validate_email])
    supervisor_name = models.ForeignKey('self', blank=True, null=True,on_delete=models.SET_NULL, db_column='supervisor_name')
    badgeNum = models.CharField(max_length=30, blank=True, null= True)
    idNumber = models.CharField(max_length=30, blank=True, null= True)
    #code = models.CharField(max_length=30, blank=True, null= True)
    Code = models.ForeignKey(Code, on_delete=models.SET_NULL, null=True, blank=True)
    gustoID = models.CharField(max_length=30, blank=True, null= True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, db_column='user')
    is_supervisor = models.BooleanField(default=False)
    photo = models.ImageField(null=True, blank=True, upload_to="employee/")

    is_admin = models.BooleanField(default=False)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.first_name + ", " + self.last_name
    
class Client(models.Model):
    EmployeeID = models.ForeignKey(Employee , on_delete=models.CASCADE, db_column ='EmployeeID', null=False, blank=False) 
    clientID =  models.CharField( max_length=30, blank=True, null= True)  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(null=True, blank=True)
    createdBy = models.CharField(max_length=60, blank=True, null=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    updatedBy = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.first_name + ", " + self.last_name


class period(models.Model):
    fromDate = models.DateField()
    toDate = models.DateField()
    payDate = models.DateField()
    status = models.IntegerField(choices = period_status_choice)
    approved_date = models.DateTimeField(null=True, blank=True)
    approvedBy = models.CharField(max_length=60, blank=True, null=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    closedBy = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return str(self.fromDate) + " - " + str(self.toDate)