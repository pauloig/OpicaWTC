from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login as login_process
from django.contrib.auth.decorators import login_required
from . import views
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from catalog import models as catalogModel

@login_required(login_url='/login/')
def home(request):
    dic = {}    
    context = {}  
    emp = catalogModel.Employee.objects.filter(user__username__exact = request.user.username).first()
    context["emp"] = emp

    if emp:       
        pbth = catalogModel.EmpType.objects.filter(empTypeID = 1).first()
        nopay = catalogModel.EmpType.objects.filter(empTypeID  = 5).first()
        #empType Paud by The Hour
        
        if emp.is_admin or request.user.is_staff:
            return render(
            request,
            'index.html',
            context        
            )
        elif (emp.EmpType.empTypeID in (1,5) and not emp.is_admin) or not hasattr(emp, 'EmpType'):
                return HttpResponseRedirect('/wtc/paidByTheHour/')
        else:
            return render(
            request,
            'index.html',
            context        
            )
            
    else:
        return HttpResponseRedirect('/wtc/paidByTheHour/')
        #dic = {'state': 2, 'message': "Login failed"}
    
    return render(request, 'login.html', dic)           

def login(request):
    state = 0
    message = ""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

       

        if user is not None:
            login_process(request, user)
            state = 1
            message = ""

            opType = "Log In"
            opDetail = "Login Successfull"

            

            return redirect('/home/')
        else:
            state = 2
            opType = "Log In"
            opDetail = "Login Failed, Username or password is incorrect - " + username + " -"

            

            message = "Username or password is incorrect"
    dic = {'state': state, 'message': message}
    return render(request, 'login.html', dic)

def prueba(request):
    status = 0

    return render(request, 'authentication/prueba.html')