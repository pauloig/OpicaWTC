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
    path('pbth_create/<periodID>/<empID>',views.pbth_create), 
    path('pbth_update/<id>/<periodID>/<empID>',views.pbth_update),
    path('pbth_remove/<id>/<periodID>/<empID>',views.pbth_RemoveSup),

    #Payd By Comission
    path('service_list/',views.service_list),
    path('create_service/',views.create_service),
    path('update_service/<id>',views.update_service), 
    path('service_remove/<id>',views.service_remove), 
    path('update_serviceSup/<id>/<periodID>/<empID>',views.update_serviceSup), 
    path('serviceSup_remove/<id>/<periodID>/<empID>',views.serviceSup_remove), 
    
    path('paidBySalaryRemoveSup/<periodID>/<id>/<empID>',views.BySalaryRemoveSup), 

    #Payd By Salary
    path('period_list/',views.period_list),
    path('period_management/<id>/',views.period_management),
    path('paidBySalary/<periodID>/<day>',views.BySalary), 
    path('paidBySalarySup/<periodID>/<empID>',views.BySalarySup), 
    path('paidBySalaryUpdate/<periodID>/<id>',views.BySalaryUpdate), 
    path('paidBySalaryUpdateSup/<periodID>/<id>/<empID>',views.BySalaryUpdateSup), 
    path('paidBySalaryRemove/<periodID>/<id>',views.BySalaryRemove), 
    path('paidBySalaryRemoveSup/<periodID>/<id>/<empID>',views.BySalaryRemoveSup), 

    #Payd By Hourly Manually
    path('period_management_manually/<id>/',views.period_management_manually),
    path('paidManually/<periodID>/<day>',views.paidManually), 
    path('paidManuallySup/<periodID>/<empID>',views.paidManuallySup), 
    path('paidManuallyUpdate/<periodID>/<id>',views.paidManuallyUpdate), 
    path('paidManuallyUpdateSup/<periodID>/<id>/<empID>',views.paidManuallyUpdateSup), 
    path('paidManuallyRemove/<periodID>/<id>',views.paidManuallyRemove), 
    path('paidManuallyRemoveSup/<periodID>/<id>/<empID>',views.paidManuallyRemoveSup), 
    
    #Admin
    path('period_admin_list/',views.period_admin_list),
    path('create_period/',views.create_period),
    path('close_period/<id>',views.close_preiod),
    path('employee_admin_list/<id>/<empType>/<empStatus>',views.employee_admin_list),
    path('employee_admin_detail/<id>/<empID>',views.employee_admin_detail),
    path('get_timesheet/<periodID>/<empID>/<empType>/<empStatus>',views.get_timesheet),
    path('get_detail/<periodID>/<empID>',views.get_detail),
    path('get_payroll/<periodID>/<empType>/<empStatus>',views.get_payroll),
    
]