from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login as login_process
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import *
from .forms import * 
from . import views
from sequences import get_next_value, Sequence
from tablib import Dataset
from django.contrib import messages

# ********************* EMPLOYEE **********************

@login_required(login_url='/home/')
def upload_employee(request):
    
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    per = period.objects.filter(status__in=(1,2)).first()

    countInserted = 0
    countRejected = 0
    countProcessed = 0
    rejectedEmp = ""

    if request.method == 'POST':
        #Employee.objects.all().delete()
        #employee_resource = Employee()
        dataset = Dataset()
        new_employees = request.FILES['myfile']

        if not new_employees.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request,'upload.html', {'countInserted':countInserted, 'countRejected':countRejected, 'Processed': countProcessed, 'rejectedEmp':rejectedEmp})

        imported_data = dataset.load(new_employees.read(),format='xlsx', read_only = False)
    
        #return render(request,'catalog/upload_employee.html',
        # {'imported_data':imported_data})
        
        for data in imported_data:  
            
            if data[0]!= None and data[0]!= "":
                
                #Getting Department Catalog 
                dep = Department.objects.filter(name__iexact = data[8].lower()).first()

                if data[9] != None and data[9] != "":
                    rate = rate * 100
                else:
                    rate = 0

                #Getting Job Title Catalog 
                job = JobTitle.objects.filter(name__iexact = data[12].lower()).first()

                #Getting EmpType Catalog 
                empt = EmpType.objects.filter(name__iexact = data[13].lower()).first()

                #Getting Supervisor Catalog 
                if data[17] != None and data[17] != "":
                    completesup = data[17].split(",")
                    first = completesup[1].strip()
                    if len(completesup) > 1 :
                        last = completesup[0]
                    else:
                        last = ""

                    sup = Employee.objects.filter(first_name = first, last_name = last).first()
                else:
                    sup = None

                empSeq = Sequence("emp", initial_value=1500) 
                empID = str(empSeq.get_next_value())      

                if data[23] == 'T' or  data[23] == 'True'  or data[23] == '1' : 
                    is_sup = True
                else:
                    is_sup = False

                emp_status = EmptStatus.objects.filter(name = 'Active').first()

                #try:         
                value = Employee(
                    employeeID =empID,
                    first_name = data[0],
                    last_name = data[1],
                    address_city = data[2],
                    address_state = data[3],
                    address_street = data[4],
                    address_zip = data[5],
                    phone_number = data[6],
                    gender = data[7],
                    Department = dep,
                    rate = rate,
                    rate_by_hour = data[10],
                    schedule_by_day = data[11],
                    JobTitle = job,
                    EmpType =empt,
                    EmptStatus = emp_status,
                    birthDate = data[14],
                    start_date = data[15],                       
                    email = data[16],
                    supervisor_name = sup,
                    badgeNum = data[18],
                    idNumber = data[19],                        
                    #Code = models.ForeignKey(Code, on_delete=models.SET_NULL, null=True, blank=True)
                    gustoID = data[21],                       
                    is_supervisor = is_sup,                                              
                    createdBy = request.user.username,
                    created_date = datetime.now()
                )
                value.save()

                

                countInserted = countInserted + 1
                """except Exception as e:
                    countRejected = countRejected + 1
                    rejectedEmp += ", " + data[14]"""
                    

            countProcessed += 1

    return render(request,'catalog/upload_employee.html', {'countInserted':countInserted, 'countRejected':countRejected,'rejectedEmp':rejectedEmp, 'emp': emp, 'per':per})
    

@login_required(login_url='/home/')
def employee_list(request, empStatus):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    if empStatus != "0" :
        empList  = Employee.objects.filter(EmptStatus__empStatusID = empStatus)
    else:
        empList = Employee.objects.all()

   
    context ={}

    context["selectedEmptStatus"] = empStatus
    context["dataset"] = empList
    context["emp"]= emp
    context["empStatus"] = EmptStatus.objects.all()
    return render(request, "catalog/employee_list.html", context)



@login_required(login_url='/home/')
def create_employee(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    context ={}

    form = EmployeesForm(request.POST or None, request.FILES)

    if form.is_valid():
        empSeq = Sequence("emp", initial_value=1500) 
        empID = str(empSeq.get_next_value())       
        form.instance.employeeID = empID
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.now()   
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/catalog/employee_list/')
        
         
    context['form']= form
    context["emp"] = emp
    return render(request, "catalog/create_employee.html", context)

@login_required(login_url='/home/')
def update_employee(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(Employee, employeeID = id)
 
    form = EmployeesForm(request.POST or None, request.FILES or None, instance = obj)
 
    if form.is_valid():
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.save()
        context["dataset"] = Employee.objects.all()  
        context["emp"] = emp       
        return HttpResponseRedirect('/catalog/employee_list/')

    context["form"] = form
    context["emp"] = emp
    return render(request, "catalog/create_employee.html", context)

# ********************* DEPARTMENT **********************
@login_required(login_url='/home/')
def department_list(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    context["dataset"] = Department.objects.all()
    context["emp"]= emp

    return render(request, "catalog/department_list.html", context)


@login_required(login_url='/home/')
def create_department(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    context ={}

    form = DepartmentForm(request.POST or None)

    if form.is_valid():
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.now()   
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/catalog/department_list/')
        
         
    context['form']= form
    context["emp"] = emp
    return render(request, "catalog/create_department.html", context)

@login_required(login_url='/home/')
def update_department(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(Department, id = id)
 
    form = DepartmentForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.save()
       
        return HttpResponseRedirect('/catalog/department_list/')

    context["form"] = form
    context["emp"] = emp
    return render(request, "catalog/create_department.html", context)


# ********************* JOB TITLE **********************
@login_required(login_url='/home/')
def jobtitle_list(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    context["dataset"] = JobTitle.objects.all()
    context["emp"]= emp

    return render(request, "catalog/jobtitle_list.html", context)


@login_required(login_url='/home/')
def create_jobtitle(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    context ={}

    form = JobTitleForm(request.POST or None)

    if form.is_valid():
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.now()   
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/catalog/jobtitle_list/')
        
         
    context['form']= form
    context["emp"] = emp
    return render(request, "catalog/create_jobtitle.html", context)

@login_required(login_url='/home/')
def update_jobtitle(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(JobTitle, id = id)
 
    form = JobTitleForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.save()
       
        return HttpResponseRedirect('/catalog/jobtitle_list/')

    context["form"] = form
    context["emp"] = emp
    return render(request, "catalog/create_jobtitle.html", context)

# ********************* CODE **********************
@login_required(login_url='/home/')
def code_list(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    context["dataset"] = Code.objects.all()
    context["emp"]= emp

    return render(request, "catalog/code_list.html", context)


@login_required(login_url='/home/')
def create_code(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    context ={}

    form = CodeForm(request.POST or None)

    if form.is_valid():
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.now()   
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/catalog/code_list/')
        
         
    context['form']= form
    context["emp"] = emp
    return render(request, "catalog/create_code.html", context)

@login_required(login_url='/home/')
def update_code(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(Code, id = id)
 
    form = CodeForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.save()
       
        return HttpResponseRedirect('/catalog/code_list/')

    context["form"] = form
    context["emp"] = emp
    return render(request, "catalog/create_code.html", context)

# ********************* CLIENT **********************
@login_required(login_url='/home/')
def client_list(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    context["dataset"] = Client.objects.filter(EmployeeID = emp)
    context["emp"]= emp

    return render(request, "catalog/client_list.html", context)


@login_required(login_url='/home/')
def create_client(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()

    context ={}

    form = ClientForm(request.POST or None, initial={'EmployeeID':emp})

    if form.is_valid():
        form.instance.createdBy = request.user.username
        form.instance.created_date = datetime.now()   
        form.save()
        # Return to Emp List
        return HttpResponseRedirect('/catalog/client_list/')
        
         
    context['form']= form
    context["emp"] = emp
    return render(request, "catalog/create_client.html", context)

@login_required(login_url='/home/')
def update_client(request, id):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    obj = get_object_or_404(Client, id = id)
 
    form = ClientForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.instance.updatedBy = request.user.username
        form.instance.updated_date = datetime.now()    
        form.save()
       
        return HttpResponseRedirect('/catalog/client_list/')

    context["form"] = form
    context["emp"] = emp
    return render(request, "catalog/create_client.html", context)