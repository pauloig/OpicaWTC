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
            wtc.save()
        elif int(type) == 3:
            wtc.breakOut = aTime.time()
            wtc.updatedBy = request.user.username
            wtc.created_date = datetime.now() 
            wtc.save()
        elif int(type) == 4:
            wtc.breakIn = aTime.time()
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

def BySalary(request, periodID, day):
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    period = catalogModel.period.objects.filter(id = periodID).first()

    aDate = period.fromDate.strftime('%Y-%m-')
    aDate += str(day)
    actualDate = datetime.strptime(aDate,'%Y-%m-%d').date()

    form = wtcForm(request.POST or None, initial ={'EmployeeID':emp, 'periodID': period, 'date':actualDate})

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


