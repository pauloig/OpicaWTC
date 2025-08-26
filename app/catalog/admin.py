from django.contrib import admin
from catalog.models import *


class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ('employeeID','first_name','last_name',)
    list_display = ('employeeID','first_name','last_name',)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department)
admin.site.register(JobTitle)
admin.site.register(Code)
admin.site.register(EmptStatus)
admin.site.register(EmpType)
admin.site.register(Client)
admin.site.register(period)
admin.site.register(periodEmployeeOvertime)

