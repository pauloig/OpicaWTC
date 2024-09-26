from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
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
def pbth_update(request, id, periodID, empID):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(wtcModel.paidByTheHour, id = id)
    
    employee = catalogModel.Employee.objects.filter(employeeID = empID).first()
 
    form = bthForm(request.POST or None, instance = obj)
 
    if form.is_valid():
    
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.save()

        return HttpResponseRedirect('/wtc/employee_admin_detail/'+ str(periodID) +"/" + str(empID))
    
    context["form"] = form
    context["emp"] = emp
    return render(request, "workTimeControl/pbth.html", context)


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

        dayList+= f"('day': {str(int(actualDay))}, 'regular': {str(i.regular_hours)}, 'vacation': {str(i.vacation_hours)}, 'sick':  {str(i.sick_hours)}, 'others':  {str(i.other_hours)}, 'id': {str(i.id)}),"

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

    form = wtcForm(request.POST or None, initial ={'EmployeeID':emp, 'periodID': period, 'date':actualDate, 'regular_hours':8, 'vacation_hours':0, 'sick_hours':0, 'other_hours':0})

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

    form = wtcSupForm(request.POST or None, initial ={'EmployeeID': empSelected, 'periodID': period, 'regular_hours':8, 'vacation_hours':0, 'sick_hours':0, 'other_hours':0})

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
def employee_admin_list(request, id):
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

        #Calculate Paid by the Hour
        bth = wtcModel.paidByTheHour.objects.filter(EmployeeID = e, date__range=[dateS, dateS2])

        total_hours = 0
        regular_hours = 0
        overtime_hours = 0
        double_time = 0
        holiday_hours = 0
        jobTitle = ''
        empType = ''

        for h in bth:

            total_hours += validate_decimals(h.total_hours)
            regular_hours += validate_decimals(h.regular_hours)
            overtime_hours += validate_decimals(h.overtime_hours)
            double_time += validate_decimals(h.double_time)
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
