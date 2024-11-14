from ast import Try, parse
import xlwt
from django.utils import timezone   
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login as login_process
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from . import models as wtcModel
from .forms import * 
from . import views
from sequences import get_next_value, Sequence 
from catalog import models as catalogModel
from catalog import forms as catalogForm
import json
import requests



# ********************* BY THE HOUR **********************
@login_required(login_url='/home/')
def paidByTheHour(request):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    context["emp"]= emp
    context["type"]= "light"
    empNumber = ""

    if request.method == "POST":
        empNumber =  request.POST.get('idNumber')
        empNumber = int(0 if empNumber is None or empNumber is "" else empNumber )

        if empNumber > 0:
            obj = catalogModel.Employee.objects.filter(badgeNum = empNumber).first()
        
            if obj:
                return HttpResponseRedirect('/wtc/pbth_form/' + str(obj.employeeID) )
            else:
                context["type"]= "danger"
                context["message"] = "Invalid Employee ID " + str(empNumber)
        
    context["timestamp"]= timezone.now().timestamp()
        
    return render(request, "workTimeControl/paidByTheHour.html", context)


@login_required(login_url='/home/')
def pbth_form(request, id):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    cInStatus = 'disabled'
    coutStatus = 'disabled'
    bOutStatus = 'disabled'
    bInStatus = 'disabled'
    lOutStatus = 'disabled'
    lInStatus = 'disabled'

    # Getting the Employee Object 
    Empobj = get_object_or_404(catalogModel.Employee, employeeID = id)

    # Getting the wtc for the day
    aDate = datetime.now().strftime('%Y-%m-%d')
    actualDate = datetime.strptime(aDate,'%Y-%m-%d').date()
    wtc = wtcModel.paidByTheHour.objects.filter(EmployeeID = Empobj, date = actualDate ).first()

    if wtc:
        if wtc.clockOut != None:
            cInStatus = 'disabled'
            coutStatus = 'disabled'
        else: 
            if is_break(wtc.breakOut, wtc.breakIn) == False and is_break( wtc.lunchOut, wtc.lunchIn) == False:
                if is_clocked(wtc.breakOut, wtc.breakIn) ==False:
                     bOutStatus = ''

                if is_clocked(wtc.lunchOut, wtc.lunchIn) ==False:
                     lOutStatus = ''

                coutStatus = ''                
            elif is_break(wtc.breakOut, wtc.breakIn):
                coutStatus = 'disabled'
                bOutStatus = 'disabled'
                bInStatus = ''
            elif is_break(wtc.lunchOut, wtc.lunchIn):
                coutStatus = 'disabled'
                lOutStatus = 'disabled'
                lInStatus = ''
    else:
        cInStatus = ''   

    context["obj"] = Empobj
    context["emp"] = emp
    context["wtc"] = wtc
    context["cInStatus"] = cInStatus
    context["cOutStatus"] = coutStatus 
    context["bOutStatus"] = bOutStatus 
    context["bInStatus"] = bInStatus 
    context["lOutStatus"] = lOutStatus 
    context["lInStatus"] = lInStatus  

    return render(request, "workTimeControl/pbth_form.html", context)


def is_break(breakOut, breakIn):
    if breakOut == None and breakIn == None:
        return False
    elif breakOut != None and breakIn != None:
        return False
    elif breakOut != None or breakIn != None:
        return True

def is_clocked(clocIn, clockOut):
    if clocIn != None and clocIn != None:
        return True
    else:
        return False


@login_required(login_url='/home/')
def pbth_setTime(request, id, empID,  type):
    
    # Getting the Employee Object 
    Empobj = get_object_or_404(catalogModel.Employee, employeeID = empID)
   
    # Getting the wtc for the day
    aDate = datetime.now().strftime('%Y-%m-%d')
    actualDate = datetime.strptime(aDate,'%Y-%m-%d').date()
    aTime = datetime.now()
    
    if int(id)==0 and int(type) == 1:
        wtc = wtcModel.paidByTheHour(date = actualDate,
                            EmployeeID = Empobj,
                            clockIn = aTime.time(),
                            createdBy = request.user.username,
                            created_date = datetime.now() )
        wtc.save()
    
 

    elif int(id) > 0:

        wtc = wtcModel.paidByTheHour.objects.filter(id = id).first()

        if int(type) == 2:
            wtc.clockOut = aTime.time()
            wtc.updatedBy = request.user.username
            wtc.created_date = datetime.now() 

            wtc.clockOut =  aTime.time()
            wtc.updatedBy = request.user.username
            wtc.created_date = datetime.now() 

            #calculate total_hours
            total_hours = calculate_hours(convert_to_military(wtc.clockIn),
                                              convert_to_military(wtc.clockOut), 
                                              convert_to_military(wtc.lunchOut), 
                                              convert_to_military(wtc.lunchIn),
                                              convert_to_military(wtc.breakOut), 
                                              convert_to_military(wtc.breakIn))
            
            wtc.total_hours = total_hours

            #validate if today is a holiday
            
            wtc.holiday_hours = 0

            if total_hours <= 8:
                wtc.regular_hours = total_hours
                wtc.double_time = 0
                wtc.overtime_hours = 0
            elif total_hours > 8  and total_hours <= 12:
                wtc.regular_hours = 8                
                wtc.overtime_hours = total_hours - 8
                wtc.double_time = 0
            elif total_hours > 12:
                wtc.regular_hours = 8                
                wtc.overtime_hours = 4
                wtc.double_time = total_hours - 12

            wtc.save()
        elif int(type) == 3:
            wtc.breakOut = aTime.time()
            wtc.updatedBy = request.user.username
            wtc.created_date = datetime.now() 
            wtc.save()
        elif int(type) == 4:
            wtc.breakIn =  aTime.time()
            wtc.updatedBy = request.user.username
            wtc.created_date = datetime.now() 
            wtc.save()
        elif int(type) == 5:
            wtc.lunchOut = aTime.time()
            wtc.updatedBy = request.user.username
            wtc.created_date = datetime.now() 
            wtc.save()
        elif int(type) == 6:            
            wtc.lunchIn = aTime.time()
            wtc.updatedBy = request.user.username
            wtc.created_date = datetime.now() 
            wtc.save()
    
    return HttpResponseRedirect('/wtc/paidByTheHour/')

@login_required(login_url='/home/')
def pbth_create(request, periodID, empID):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    period = catalogModel.period.objects.filter(id = periodID).first()

    empSelected = catalogModel.Employee.objects.filter(employeeID = empID).first()

    form = bthForm(request.POST or None, initial ={'EmployeeID': empSelected})

    if form.is_valid():
        form.instance.employeeID = emp
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.now()   
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/wtc/employee_admin_detail/'+ str(period.id) +"/" + str(empID))
    
         
    context['form']= form
    context["emp"] = emp
    return render(request, "workTimeControl/pbth.html", context)

@login_required(login_url='/home/')
def pbth_update(request, id, periodID, empID):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(wtcModel.paidByTheHour, id = id)
    
    employee = catalogModel.Employee.objects.filter(employeeID = empID).first()

    if employee:
        context["schedule"] = employee.schedule_by_day
 
    form = bthForm(request.POST or None, instance = obj)
 
    if form.is_valid():
    
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.save()

        return HttpResponseRedirect('/wtc/employee_admin_detail/'+ str(periodID) +"/" + str(empID))
    
    context["form"] = form
    context["periodID"] = periodID
    context["empID"] = empID
    context["emp"] = emp
    return render(request, "workTimeControl/pbth.html", context)

@login_required(login_url='/home/')
def pbth_RemoveSup(request, id, periodID, empID):    

    obj = get_object_or_404(wtcModel.paidByTheHour,id = id)

    if obj:
        obj.delete()
        
    return HttpResponseRedirect('/wtc/employee_admin_detail/'+ str(periodID) +"/" + str(empID))


# ********************* PAID BY COMISSION **********************
@login_required(login_url='/home/')
def service_list(request):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    context["dataset"] = paidByComission.objects.all()
    context["emp"]= emp

    return render(request, "workTimeControl/service_list.html", context)

@login_required(login_url='/home/')
def create_service(request):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()

    context ={}

    clientObj = catalogModel.Client.objects.filter(EmployeeID = emp)

    form = ServiceForm(request.POST or None, initial ={'EmployeeID':emp}, qs = clientObj)

    if form.is_valid():
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.now()   
        form.instance.rate = emp.rate
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/wtc/service_list/')
    
         
    context['form']= form
    context["emp"] = emp
    return render(request, "workTimeControl/create_service.html", context)

@login_required(login_url='/home/')
def update_service(request, id):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(paidByComission, id = id)

    clientObj = catalogModel.Client.objects.filter(EmployeeID = emp)
 
    form = ServiceForm(request.POST or None, instance = obj, qs = clientObj)
 
    if form.is_valid():
    
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.instance.rate = emp.rate
        form.save()

        return HttpResponseRedirect('/wtc/service_list/')

    context["form"] = form
    context["emp"] = emp
    return render(request, "workTimeControl/create_service.html", context)

@login_required(login_url='/home/')
def update_serviceSup(request, id, periodID, empID):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(paidByComission, id = id)
    
    employee = catalogModel.Employee.objects.filter(employeeID = empID).first()
    clientObj = catalogModel.Client.objects.filter(EmployeeID = employee)
 
    form = ServiceForm(request.POST or None, instance = obj, qs = clientObj)
 
    if form.is_valid():
    
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.instance.rate = employee.rate
        form.save()

        return HttpResponseRedirect('/wtc/employee_admin_detail/'+ str(periodID) +"/" + str(empID))
    
    context["form"] = form
    context["emp"] = emp
    return render(request, "workTimeControl/create_serviceSup.html", context)

# ********************* PAID BY SALARY **********************
@login_required(login_url='/home/')
def period_list(request):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    context["dataset"] = catalogModel.period.objects.all()
    context["emp"]= emp

    return render(request, "workTimeControl/period_list.html", context)

@login_required(login_url='/home/')
def period_management(request, id):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    period = catalogModel.period.objects.filter(id=id).first()
    days = paidBySalary.objects.filter(periodID = period, EmployeeID = emp).all()
    dayList = "["



    for i in days:

        actualDay = i.date.strftime("%d")

        dayList+= f"('day': {str(int(actualDay))}, 'regular': {str(i.regular_hours)}, 'vacation': {str(i.vacation_hours)}, 'sick':  {str(i.sick_hours)}, 'holiday':  {validate_decimals(i.holiday_hours)}, 'others':  {str(i.other_hours)}, 'id': {str(i.id)}),"

    dayList += "]"


    context["period"] = period
    context["days"] = dayList
    context["emp"]= emp

    return render(request, "workTimeControl/period_management.html", context)

@login_required(login_url='/home/')
def BySalary(request, periodID, day):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    period = catalogModel.period.objects.filter(id = periodID).first()

    aDate = period.fromDate.strftime('%Y-%m-')
    aDate += str(day)
    actualDate = datetime.strptime(aDate,'%Y-%m-%d').date()

    form = wtcForm(request.POST or None, initial ={'EmployeeID':emp, 'periodID': period, 'date':actualDate, 'regular_hours':8, 'vacation_hours':0, 'sick_hours':0, 'holiday_hours': 0, 'other_hours':0})

    if form.is_valid():
        form.instance.employeeID = emp
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.now()   
        form.instance.status = 1
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/wtc/period_management/'+ str(periodID))
    
         
    context['form']= form
    context["emp"] = emp
    return render(request, "workTimeControl/paidBySalary.html", context)

@login_required(login_url='/home/')
def BySalarySup(request, periodID, empID):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    period = catalogModel.period.objects.filter(id = periodID).first()

    #aDate = period.fromDate.strftime('%Y-%m-')
    #aDate += str(day)
    #actualDate = datetime.strptime(aDate,'%Y-%m-%d').date()

    empSelected = catalogModel.Employee.objects.filter(employeeID = empID).first()

    form = wtcSupForm(request.POST or None, initial ={'EmployeeID': empSelected, 'periodID': period, 'regular_hours':8, 'vacation_hours':0, 'sick_hours':0, 'holiday_hours':0,'other_hours':0})

    if form.is_valid():
        form.instance.employeeID = emp
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.now()   
        form.instance.status = 1
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/wtc/employee_admin_detail/'+ str(period.id) +"/" + str(empID))
    
         
    context['form']= form
    context["emp"] = emp
    return render(request, "workTimeControl/paidBySalary.html", context)

@login_required(login_url='/home/')
def BySalaryUpdate(request, periodID, id):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(paidBySalary,id = id)
    obj.holiday_hours = validate_decimals(obj.holiday_hours)
    obj.save()

    form = wtcForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/wtc/period_management/'+ str(periodID))
    
         
    context['form']= form
    context["emp"] = emp
    return render(request, "workTimeControl/paidBySalary.html", context)


@login_required(login_url='/home/')
def BySalaryUpdateSup(request, periodID, id, empID):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(paidBySalary,id = id)
    obj.holiday_hours = int(validate_decimals(obj.holiday_hours))
    obj.save()

    form = wtcForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/wtc/employee_admin_detail/'+ str(periodID) +"/" + str(empID))
    
    
         
    context['form']= form
    context["emp"] = emp
    context["empID"] = empID
    return render(request, "workTimeControl/paidBySalary.html", context)

@login_required(login_url='/home/')
def BySalaryRemove(request, periodID, id):    

    obj = get_object_or_404(paidBySalary,id = id)

    if obj:
        obj.delete()
        
    return HttpResponseRedirect('/wtc/period_management/'+ str(periodID))   

@login_required(login_url='/home/')
def BySalaryRemoveSup(request, periodID, id, empID):    

    obj = get_object_or_404(paidBySalary,id = id)

    if obj:
        obj.delete()
        
    return HttpResponseRedirect('/wtc/employee_admin_detail/'+ str(periodID) +"/" + str(empID))


# ************************* ADMIN ***********************************

@login_required(login_url='/home/')
def period_admin_list(request):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    context["dataset"] = catalogModel.period.objects.all()
    context["emp"]= emp

    return render(request, "workTimeControl/period_admin_list.html", context)

@login_required(login_url='/home/')
def employee_admin_list(request, id, download = False):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    report = []
    employeeList  = catalogModel.Employee.objects.all()
    
    period = catalogModel.period.objects.filter(id = id).first()

    """dateSelected =  period.fromDate
    dateSelected2 = period.toDate
    dateS = datetime.strptime(dateSelected, '%Y-%m-%d').date()
    dateS2 = datetime.strptime(dateSelected2, '%Y-%m-%d').date()"""
    
    dateS = period.fromDate
    dateS2 = period.toDate

    for e in employeeList:        

        total_hours = 0
        regular_hours = 0
        overtime_hours = 0
        double_time = 0
        holiday_hours = 0
        jobTitle = ''
        empType = ''

        if e.EmpType:
            # Employe Type --> Paid By the Hour
            if e.EmpType.empTypeID == 1:    

                #Calculate Paid by the Hour
                bth = wtcModel.paidByTheHour.objects.filter(EmployeeID = e, date__range=[dateS, dateS2])

                for h in bth:
                    total_hours += validate_decimals(h.total_hours)
                    regular_hours += validate_decimals(h.total_hours)
                    overtime_hours += validate_decimals(h.overtime_hours)
                    double_time += validate_decimals(h.double_time)
                    holiday_hours += validate_decimals(h.holiday_hours)

            # Employe Type --> Paid By Salary
            elif e.EmpType.empTypeID == 3: 
                #Calculate Paid by Salary
                bth = wtcModel.paidBySalary.objects.filter(EmployeeID = e, date__range=[dateS, dateS2])

                for h in bth:
                    total_hours += validate_decimals(h.regular_hours) + validate_decimals(h.vacation_hours) + validate_decimals(h.sick_hours) + validate_decimals(h.other_hours)
                    regular_hours += validate_decimals(h.regular_hours) + validate_decimals(h.vacation_hours) + validate_decimals(h.sick_hours) + validate_decimals(h.other_hours)
                    overtime_hours += 0
                    double_time += 0
                    holiday_hours += validate_decimals(h.holiday_hours)

            
            
            if e.JobTitle != None:
                jobTitle = e.JobTitle.name
            
            if e.EmpType != None:
                empType = e.EmpType.name

            #Calculate Paid by Comission
            bc = wtcModel.paidByComission.objects.filter(EmployeeID = e, payment_date__range=[dateS, dateS2])
            
            payout_due = 0

            for ec in bc:
                payout_due += (ec.payment_amount * ec.rate)/100

            report.append({'empID':e.employeeID ,'last_name': e.last_name, 'first_name': e.first_name, 'title': jobTitle , 'gusto_id': e.gustoID, 'employee_type': empType,
                        'total_hours' : total_hours, 'regular_hours' : regular_hours, 
                        'overtime_hours' : overtime_hours, 'double_time' : double_time, 'holiday_hours' : holiday_hours, 'custom': payout_due})
                            

    if download:
        return report
    
    
    context["dataset"] = report
    context["emp"]= emp
    context["period"] = period 
    return render(request, "workTimeControl/employee_admin_list.html", context)

@login_required(login_url='/home/')
def employee_admin_detail(request, id, empID):
    
    context ={}
    bth = None
    bc = None
    bs = None

    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    period = catalogModel.period.objects.filter(id = id).first()
    dateS = period.fromDate
    dateS2 = period.toDate

    employee = catalogModel.Employee.objects.filter(employeeID = empID).first()

    # Employe Type --> Paid By the Hour
    if employee.EmpType.empTypeID == 1:    

        #Calculate Paid by the Hour
        bth = wtcModel.paidByTheHour.objects.filter(EmployeeID = employee, date__range=[dateS, dateS2])

    # Employe Type --> Paid By Salary
    elif employee.EmpType.empTypeID == 3: 
        #Calculate Paid by Salary
        bs = wtcModel.paidBySalary.objects.filter(EmployeeID = employee, date__range=[dateS, dateS2])

    #Calculate Paid by Comission
    bc = wtcModel.paidByComission.objects.filter(EmployeeID = employee, payment_date__range=[dateS, dateS2])

    
    context["hour"] = bth
    context["salary"] = bs
    context["comission"] = bc
    context["emp"]= emp
    context["employee"]= employee
    context["period"] = period 
    return render(request, "workTimeControl/employee_admin_detail.html", context)

@login_required(login_url='/home/')
def get_timesheet(request, periodID, empID):
    

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('timesheet', cell_overwrite_ok = True) 

    

    # Sheet header, first row
    row_num = 4

    font_title = xlwt.XFStyle()
    font_title.font.bold = True
    font_title = xlwt.easyxf('font: bold on, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white;')

    
    font_style =  xlwt.XFStyle()              

    font_title2 = xlwt.easyxf('font: bold on, height 480, color black;\
                                align: horiz center;\
                                pattern: pattern solid, fore_color white;')
    
    font_title3 = xlwt.easyxf('font:  height 400, color black;\
                                align: horiz center;\
                                pattern: pattern solid, fore_color white;')
    
    font_title4 = xlwt.easyxf('font:  height 300, color black;\
                                align: horiz center, vertical center;\
                              borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                                pattern: pattern solid, fore_color white;')

    font_title5 = xlwt.easyxf('font:  height 200, color black;\
                            align: horiz left;\
                            borders: top_color black, bottom_color black, right_color black, left_color black,\
                            left thin, right thin, top thin, bottom thin;\
                            pattern: pattern solid, fore_color white;')


    period = catalogModel.period.objects.filter(id = periodID).first()
    emplo = catalogModel.Employee.objects.filter(employeeID = empID).first()


    ws.write_merge(0, 0, 0, 5, 'OPICA Employee Time Sheet ',font_title2)   
    ws.write_merge(1, 1, 0, 5, emplo.first_name + ' '+ emplo.last_name ,font_title3) 
    ws.write_merge(3, 4, 0, 1, 'PAY DATE: ',font_title4) 
    ws.write_merge(5, 5, 0, 1, 'HOURS WORKED-LESS LUNCH',font_title5) 
    ws.write_merge(6, 6, 0, 1, 'HOURS SCHEDULED-LESS LUNCH',font_title5) 
    ws.write_merge(7, 7, 0, 1, 'COMMISIONS',font_title5) 
    ws.write_merge(9, 9, 0, 1, 'VACATION',font_title5) 
    ws.write_merge(10, 10, 0, 1, 'SICK',font_title5) 
    ws.write_merge(11, 11, 0, 1, 'HOLIDAY',font_title5) 
    ws.write_merge(12, 12, 0, 1, 'OTHERS',font_title5) 
    ws.write_merge(13, 13, 0, 1, '',font_title5) 
    ws.write_merge(14, 14, 0, 1, '',font_title5) 
    ws.write_merge(16, 16, 0, 1, 'NO-PAY',font_title5) 

                   

    period = catalogModel.period.objects.filter(id = periodID).first()

    days = int((period.toDate - period.fromDate).days) + 1

    vacation = 0
    sick = 0
    holiday = 0
    others = 0
    total = 0
    commision = 0


    for col_num in range(days):
        actual = period.fromDate + timedelta(days=col_num)
        ws.write(row_num-1, col_num+2, str(actual.strftime("%a").upper()), font_title)
        ws.write(row_num, col_num+2, str(actual.strftime("%m/%d")), font_title) 
        
        #Setting up the total hours for the current day
        
        # if the current day is not Saturday or Sunday
    
        if str(actual.strftime("%a").upper()) == 'SUN' or str(actual.strftime("%a").upper()) == 'SAT':

            ws.write(5, col_num+2,'' , font_title) 
            ws.write(6, col_num+2,'' , font_title) 
            ws.write(7, col_num+2,'' , font_title) 
            ws.write(9, col_num+2,'' , font_title) 
            ws.write(10, col_num+2,'' , font_title) 
            ws.write(11, col_num+2,'' , font_title) 
            ws.write(12, col_num+2,'' , font_title) 
            ws.write(13, col_num+2,'' , font_title) 
            ws.write(14, col_num+2,'' , font_title) 
            ws.write(16, col_num+2,'' , font_title) 
        else:

            current = wtcModel.paidByTheHour.objects.filter(EmployeeID = emplo, date = actual).first()

            if current:
                if validate_decimals(current.sick_hours) == 0 and validate_decimals(current.vacation_hours) == 0 and validate_decimals(current.holiday_hours) == 0 and validate_decimals(current.other_hours) == 0:
                    ws.write(5, col_num+2,validate_decimals(current.total_hours) , font_title5)
                    total += validate_decimals(current.total_hours)
                else:
                    ws.write(5, col_num+2,'' , font_title5)

                #Vacation
                if validate_decimals(current.vacation_hours) == 0:
                    ws.write(9, col_num+2,'' , font_title5) 
                else:
                    ws.write(9, col_num+2,validate_decimals(current.vacation_hours), font_title5) 
                    vacation += validate_decimals(current.vacation_hours)
                
                #Sick
                if validate_decimals(current.sick_hours) == 0:
                    ws.write(10, col_num+2,'' , font_title5) 
                else:
                    ws.write(10, col_num+2,validate_decimals(current.sick_hours), font_title5) 
                    sick += validate_decimals(current.sick_hours)

                #Holiday
                if validate_decimals(current.holiday_hours) == 0:
                    ws.write(11, col_num+2,'' , font_title5) 
                else:
                    ws.write(11, col_num+2,validate_decimals(current.holiday_hours), font_title5)  
                    holiday += validate_decimals(current.holiday_hours)

                #Others
                if validate_decimals(current.other_hours) == 0:
                    ws.write(12, col_num+2,'' , font_title5) 
                else:
                    ws.write(12, col_num+2,validate_decimals(current.other_hours), font_title5) 
                    others += validate_decimals(current.other_hours)


            else:
                ws.write(5, col_num+2,'' , font_title5)    
                ws.write(9, col_num+2,'' , font_title) 
                ws.write(10, col_num+2,'' , font_title) 
                ws.write(11, col_num+2,'' , font_title) 
                ws.write(12, col_num+2,'' , font_title)          
            
            # Scheduled Hours
            ws.write(6, col_num+2,validate_decimals(emplo.schedule_by_day) , font_title5) 

                         
            ws.write(13, col_num+2,'' , font_title5) 
            ws.write(14, col_num+2,'' , font_title5) 
            ws.write(16, col_num+2,'' , font_title5) 

            #Calculate Comission
            comm = wtcModel.paidByComission.objects.filter(EmployeeID = emplo, payment_date = actual)
            actual_comm = 0
            for c in comm:
                if (validate_decimals(c.payment_amount) * validate_decimals(c.rate)) > 0: 
                    actual_comm += (validate_decimals(c.payment_amount) * validate_decimals(c.rate)) / 100


            if validate_decimals(actual_comm) > 0:
                ws.write(7, col_num+2, validate_decimals(actual_comm) , font_title5)
            else:
                ws.write(7, col_num+2,'' , font_title5)

            commision += actual_comm


    ws.write_merge(row_num-1, row_num, days+2, days+2, 'Sub Total',font_title) 
    ws.write_merge(5, 5, days+2, days+2, validate_decimals(total),font_title) 
    ws.write_merge(6, 6, days+2, days+2, '',font_title) 
    ws.write_merge(7, 7, days+2, days+2, validate_decimals(commision),font_title) 
    ws.write_merge(9, 9, days+2, days+2, validate_decimals(vacation),font_title) 
    ws.write_merge(10, 10, days+2, days+2, validate_decimals(sick),font_title) 
    ws.write_merge(11, 11, days+2, days+2, validate_decimals(holiday),font_title) 
    ws.write_merge(12, 12, days+2, days+2, validate_decimals(others),font_title) 
    ws.write_merge(13, 13, days+2, days+2, '-',font_title) 
    ws.write_merge(14, 14, days+2, days+2, '-',font_title) 
    ws.write_merge(16, 16, days+2, days+2, '-',font_title) 

    ws.write_merge(18, 18, 2, 6, 'TOTAL HOURS',font_title4) 
    ws.write_merge(18, 18, 7, 8, validate_decimals(total + vacation + sick + holiday + others),font_title4) 



    ws.write_merge(19, 19, 2, 6, 'TOTAL COMISSIONS',font_title4) 
    ws.write_merge(19, 19, 7, 8, validate_decimals(commision),font_title4) 


    ws.write_merge(21, 24, 0, 0, 'COMMENTS',font_title4) 
    ws.write_merge(21, 21, 1, 16, '',font_title4) 
    ws.write_merge(22, 22, 1, 16, '',font_title4) 
    ws.write_merge(23, 23, 1, 16, '',font_title4) 
    ws.write_merge(24, 24, 1, 16, '',font_title4) 

    ws.write_merge(26, 27, 0, 1, 'EMPLOYEE  SIGNATURE',font_title5) 
    ws.write_merge(26, 27, 2, 9, '',font_title5) 
    ws.write_merge(26, 27, 10, 11, 'DATE',font_title5) 
    ws.write_merge(26, 27, 12, 16, '',font_title5) 

    ws.write_merge(28, 29, 0, 1, 'AUTHORIZED SIGNATURE',font_title5) 
    ws.write_merge(28, 29, 2, 9, '',font_title5) 
    ws.write_merge(28, 29, 10, 11, 'DATE',font_title5) 
    ws.write_merge(28, 29, 12, 16, '',font_title5)     

    ws.write_merge(30, 31, 0, 1, 'EXECUTIVE DIRECTOR SIGNATURE',font_title5) 
    ws.write_merge(30, 31, 2, 9, '',font_title5) 
    ws.write_merge(30, 31, 10, 11, 'DATE',font_title5) 
    ws.write_merge(30, 31, 12, 16, '',font_title5) 
    



    #ordenes = woInvoice.objects.filter(created_date__year = datetime.strftime(dateS, '%Y'), created_date__month = datetime.strftime(dateS, '%m'))

       

            
    ws.col(0).width = 6000
    ws.col(1).width = 6000

    for i in range(15):
        ws.col(i+2).width = 1800
   
    ws.col(days+2).width = 3000
 

    filename = 'Employee report.xls'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename 

    wb.save(response)

    return response


@login_required(login_url='/home/')
def get_payroll(request, periodID):
    
    period = catalogModel.period.objects.filter(id = periodID).first()

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Payroll ' + str(period.fromDate.strftime("%Y%m%d")) + '-' + str(period.toDate.strftime("%Y%m%d")), cell_overwrite_ok = True) 

    

    # Sheet header, first row
    row_num = 0

    font_title = xlwt.XFStyle()
    font_title.font.bold = True
    font_title = xlwt.easyxf('font: bold on, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white;')

    
    font_style =  xlwt.XFStyle()              

    font_title2 = xlwt.easyxf('font: bold on, height 480, color black;\
                                align: horiz center;\
                                pattern: pattern solid, fore_color white;')
    
    font_title3 = xlwt.easyxf('font:  height 400, color black;\
                                align: horiz center;\
                                pattern: pattern solid, fore_color white;')
    
    font_title4 = xlwt.easyxf('font:  height 300, color black;\
                                align: horiz center, vertical center;\
                              borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                                pattern: pattern solid, fore_color white;')

    font_title5 = xlwt.easyxf('font:  height 200, color black;\
                            align: horiz left;\
                            borders: top_color black, bottom_color black, right_color black, left_color black,\
                            left thin, right thin, top thin, bottom thin;\
                            pattern: pattern solid, fore_color white;')


    
    days = int((period.toDate - period.fromDate).days) + 1




    #ordenes = woInvoice.objects.filter(created_date__year = datetime.strftime(dateS, '%Y'), created_date__month = datetime.strftime(dateS, '%m'))


    #Adding the Column Title
    columns = ['last_name','first_name' ,'title', 'gusto_employee_id', 'regular_hours', 'overtime_hours','double_overtime_hours','holiday_hours','bonus', 'commission','paycheck_tips','cash_tips','correction_payment', 'custom_earning_counseling_earnings_60', 'reimbursement', 'personal_note' ] 

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_title) 
    
    list = employee_admin_list(request, periodID, True)

    for i in list:
        row_num += 1
        ws.write(row_num, 0,str(i['last_name']), font_title5) 
        ws.write(row_num, 1,str(i['first_name']), font_title5) 
        ws.write(row_num, 2,str(i['title']), font_title5) 
        ws.write(row_num, 3,str(i['gusto_id']), font_title5) 
        ws.write(row_num, 4,str(i['regular_hours']), font_title5) 
        ws.write(row_num, 5,str(i['overtime_hours']), font_title5) 
        ws.write(row_num, 6,str(i['double_time']), font_title5) 
        ws.write(row_num, 7,str(i['holiday_hours']), font_title5) 
        ws.write(row_num, 8,'', font_title5) 
        ws.write(row_num, 9,str(i['custom']), font_title5) 
        ws.write(row_num, 10,'', font_title5) 
        ws.write(row_num, 11,'', font_title5) 
        ws.write(row_num, 12,'', font_title5) 
        ws.write(row_num, 13,'', font_title5) 
        ws.write(row_num, 14,'', font_title5) 
        ws.write(row_num, 15,'', font_title5) 
       

      

            
    ws.col(0).width = 6000
    ws.col(1).width = 6000
    ws.col(2).width = 10000

    for i in range(15):
        ws.col(i+3).width = 4500
   
    ws.col(15).width = 6000
 
    rango = 'Payroll ' + str(period.fromDate.strftime("%Y%m%d")) + '-' + str(period.toDate.strftime("%Y%m%d"))
                
    filename = rango + '.xls'
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + filename 

    wb.save(response)

    return response

# -------------------- UTILITIES ----------------
def validate_decimals(value):
    try:
        return round(float(str(value)), 2)
    except:
       return 0

def convert_to_military(time):

    # Check if the input is None
    if time is None:
        return 0
    

    # Use the datetime library to parse the time and convert it
    from datetime import datetime

    time_str = time.strftime('%I:%M %p')

    # Parse the input time string (assumes format "HH:MM AM/PM")
    time_obj = datetime.strptime(time_str, '%I:%M %p')

    # Convert to military time and return the formatted string as HHMM
    return validate_decimals(time_obj.strftime('%H%M'))


def calculate_hours(startTime, endTime, lunch_startTime, lunch_endTime, break_startTime, break_endTime):
    
    if startTime != None and endTime != None:
        if startTime > endTime:
            total = 0
        else:
            #convert to decimal
            startTime = startTime/100
            st_h = int(startTime) 
            st_m = validate_decimals(startTime % 1)* 100
            st_total = validate_decimals(st_h + validate_decimals(st_m / 60))
            
            endTime = endTime / 100
            et_h = int(endTime) 
            et_m = validate_decimals(endTime % 1)* 100
            et_total = validate_decimals(et_h + validate_decimals(et_m / 60))
            
            total = et_total - st_total
    else:
        total = 0 
    
    if lunch_startTime != None and lunch_endTime != None:
        lunch_startTime = lunch_startTime / 100
        lunch_endTime = lunch_endTime / 100
        
        if lunch_startTime > lunch_endTime:
            total_lunch = 0
        elif lunch_startTime > endTime or lunch_endTime > endTime:
            total_lunch = 0
        else:
            #convert to decimal
            lst_h = int(lunch_startTime) 
            lst_m = validate_decimals(lunch_startTime % 1) * 100
            lst_total = validate_decimals(lst_h + validate_decimals(lst_m / 60))
            
            let_h = int(lunch_endTime) 
            let_m = validate_decimals(lunch_endTime % 1)* 100
            let_total = validate_decimals(let_h + validate_decimals(let_m / 60))
            
            total_lunch = let_total - lst_total
    else:
        total_lunch = 0

    if break_startTime != None and break_endTime != None:
        break_startTime = break_startTime / 100
        break_endTime = break_endTime / 100
        
        if break_startTime > break_endTime:
            total_break = 0
        elif break_startTime > endTime or break_endTime > endTime:
            total_break = 0
        else:
            #convert to decimal
            bst_h = int(break_startTime) 
            bst_m = validate_decimals(break_startTime % 1) * 100
            bst_total = validate_decimals(bst_h + validate_decimals(bst_m / 60))
            
            bet_h = int(break_endTime) 
            bet_m = validate_decimals(break_endTime % 1)* 100
            bet_total = validate_decimals(bet_h + validate_decimals(bet_m / 60))
            
            total_break = bet_total - bst_total
    else:
        total_break = 0
    
    endTotal = total - total_lunch - total_break

    return endTotal
