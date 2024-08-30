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

# ********************* EMPLOYEE **********************
@login_required(login_url='/home/')
def employee_list(request):
    emp = Employee.objects.filter(user__username__exact = request.user.username).first()
    context ={}

    context["dataset"] = Employee.objects.all()
    context["emp"]= emp

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