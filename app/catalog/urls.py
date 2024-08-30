from turtle import home
from django.contrib import admin
from django.urls import path, include
from . import views
from catalog import views

urlpatterns = [
    
    #Employee
    path('employee_list/',views.employee_list),
    path('create_employee/',views.create_employee),
    path('update_employee/<id>',views.update_employee),    
     #Department
    path('department_list/',views.department_list),
    path('create_department/',views.create_department),
    path('update_department/<id>',views.update_department),  
     #Job Title
    path('jobtitle_list/',views.jobtitle_list),
    path('create_jobtitle/',views.create_jobtitle),
    path('update_jobtitle/<id>',views.update_jobtitle),  
     #Code
    path('code_list/',views.code_list),
    path('create_code/',views.create_code),
    path('update_code/<id>',views.update_code),  
    #Client
    path('client_list/',views.client_list),
    path('create_client/',views.create_client),
    path('update_client/<id>',views.update_client), 
]