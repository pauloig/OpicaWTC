from turtle import home
from django.contrib import admin
from django.urls import path, include
from . import views
from workTimeControl import views

urlpatterns = [
    
    #paidByTheHour
    path('paidByTheHour/',views.paidByTheHour),
    path('pbth_form/<id>/',views.pbth_form),
    path('pbth_setTime/<id>/<empID>/<type>/',views.pbth_setTime),

    #Payd By Comission
    path('service_list/',views.service_list),
    path('create_service/',views.create_service),
    path('update_service/<id>',views.update_service), 

     #Payd By Comission
    path('period_list/',views.period_list),
    path('period_management/<id>/',views.period_management),
    path('paidBySalary/<periodID>/<day>',views.BySalary), 
    path('paidBySalaryUpdate/<periodID>/<id>',views.BySalaryUpdate), 
    
    
]