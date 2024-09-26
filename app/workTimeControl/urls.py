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
    path('pbth_update/<id>/<periodID>/<empID>',views.pbth_update),

    #Payd By Comission
    path('service_list/',views.service_list),
    path('create_service/',views.create_service),
    path('update_service/<id>',views.update_service), 
    path('update_serviceSup/<id>/<periodID>/<empID>',views.update_serviceSup), 

     #Payd By Salary
    path('period_list/',views.period_list),
    path('period_management/<id>/',views.period_management),
    path('paidBySalary/<periodID>/<day>',views.BySalary), 
    path('paidBySalarySup/<periodID>/<empID>',views.BySalarySup), 
    path('paidBySalaryUpdate/<periodID>/<id>',views.BySalaryUpdate), 
    path('paidBySalaryUpdateSup/<periodID>/<id>/<empID>',views.BySalaryUpdateSup), 
    path('paidBySalaryRemove/<periodID>/<id>',views.BySalaryRemove), 
    path('paidBySalaryRemoveSup/<periodID>/<id>/<empID>',views.BySalaryRemoveSup), 
    
    #Admin
    path('period_admin_list/',views.period_admin_list),
    path('employee_admin_list/<id>',views.employee_admin_list),
    path('employee_admin_detail/<id>/<empID>',views.employee_admin_detail),
    
]