import re
from types import CoroutineType
from django import forms
from .models import *

class EmployeesForm(forms.ModelForm):   

    employeeID = forms.CharField(required=False)
    supervisor_name = forms.ModelChoiceField(queryset=Employee.objects.filter(is_supervisor=True, EmptStatus = 1),required=False)
    photo = forms.ImageField(label="employee_photo", widget=forms.FileInput(), required=False)

    class Meta:
        model = Employee
        fields = [
            'employeeID',
            'first_name',
            'last_name',
            'address_city',
            'address_state',
            'address_street',
            'address_zip',
            'phone_number',
            'gender',
            'Department',
            'rate',
            'JobTitle',
            'EmpType',
            'EmptStatus',
            'birthDate',
            'start_date',
            'end_date', 
            'email',
            'supervisor_name',
            'idNumber',
            'badgeNum',
            'code',
            'gustoID',
            'user',
            'is_supervisor',
            'photo',
            'is_admin',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employeeID'].disabled = True


class DepartmentForm(forms.ModelForm):   
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_active= forms.BooleanField(required=False)
    createdBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    created_date = forms.DateField(label="Created Date", widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}), required=False)
    updatedBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    updated_date = forms.DateField(label="Updated Date", widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}),  required=False)

    class Meta:
        model = Department
        fields = [           
            "name",           
            "description",            
            'is_active',
            'createdBy',
            'created_date',
            'updatedBy',
            'updated_date',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['createdBy'].disabled = True
        self.fields['created_date'].disabled = True
        self.fields['updatedBy'].disabled = True
        self.fields['updated_date'].disabled = True
    
class JobTitleForm(forms.ModelForm):   
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_active= forms.BooleanField(required=False)
    createdBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    created_date = forms.DateField(label="Created Date", widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}), required=False)
    updatedBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    updated_date = forms.DateField(label="Updated Date", widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}),  required=False)

    class Meta:
        model = JobTitle
        fields = [           
            "name",           
            "description",            
            'is_active',
            'createdBy',
            'created_date',
            'updatedBy',
            'updated_date',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['createdBy'].disabled = True
        self.fields['created_date'].disabled = True
        self.fields['updatedBy'].disabled = True
        self.fields['updated_date'].disabled = True

class CodeForm(forms.ModelForm):   
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_active= forms.BooleanField(required=False)
    createdBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    created_date = forms.DateField(label="Created Date", widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}), required=False)
    updatedBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    updated_date = forms.DateField(label="Updated Date", widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}),  required=False)

    class Meta:
        model = Code
        fields = [           
            "name",           
            "description",            
            'is_active',
            'createdBy',
            'created_date',
            'updatedBy',
            'updated_date',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['createdBy'].disabled = True
        self.fields['created_date'].disabled = True
        self.fields['updatedBy'].disabled = True
        self.fields['updated_date'].disabled = True

class ClientForm(forms.ModelForm):  
    clientID = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    is_active= forms.BooleanField(required=False)
    createdBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    created_date = forms.DateField(label="Created Date", widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}), required=False)
    updatedBy = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    updated_date = forms.DateField(label="Updated Date", widget=forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','type': 'date'}),  required=False)

    class Meta:
        model = Client
        fields = [    
            "EmployeeID",
            "clientID",           
            "first_name",            
            "last_name",            
            'is_active',
            'createdBy',
            'created_date',
            'updatedBy',
            'updated_date',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['EmployeeID'].disabled = True
        self.fields['EmployeeID'].hidden = True
        self.fields['createdBy'].disabled = True
        self.fields['created_date'].disabled = True
        self.fields['updatedBy'].disabled = True
        self.fields['updated_date'].disabled = True
