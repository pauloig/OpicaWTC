from django.contrib import admin
from .models import *

class paidByTheHourAdmin(admin.ModelAdmin):
    list_filter = ('date','EmployeeID',)
    list_display = ('date', 'EmployeeID', 'total_hours',  'created_date', 'createdBy', 'updated_date', 'updatedBy')


class paidByComissionAdmin(admin.ModelAdmin):
    list_filter = ('payment_date','EmployeeID', 'ClientID',)
    list_display = ('payment_date', 'EmployeeID', 'ClientID', 'payment_amount', 'created_date', )

class paidBySalaryAdmin(admin.ModelAdmin):
    list_filter = ('date','EmployeeID',)
    list_display = ('date', 'EmployeeID', 'regular_hours')

admin.site.register(paidByTheHour, paidByTheHourAdmin)
admin.site.register(paidByComission, paidByComissionAdmin)
admin.site.register(paidBySalary, paidBySalaryAdmin)