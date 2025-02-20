import re
from types import CoroutineType
from django import forms
from .models import *
from catalog import models as catalogModel

class ServiceForm(forms.ModelForm):      
    

    class Meta:
        model = paidByComission
        fields = [   
            'EmployeeID',        
            "ClientID",           
            'service_date',
            'payment_date',
            'payment_number',
            'payment_method',
            'payment_card',
            'payment_amount',
            'rate',
            'createdBy',
            'created_date',
            'updatedBy',
            'updated_date',
        ]

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs')
        super().__init__(*args, **kwargs)
        self.fields["ClientID"].queryset = qs
        self.fields['createdBy'].disabled = True
        self.fields['created_date'].disabled = True
        self.fields['updatedBy'].disabled = True
        self.fields['rate'].disabled = True
        self.fields['rate'].required = False
        self.fields['updated_date'].disabled = True
        self.fields['EmployeeID'].disabled = True

class wtcForm(forms.ModelForm):      
    

    class Meta:
        model = paidBySalary
        fields = [   
            'EmployeeID',  
            'periodID',
            'date',        
            "regular_hours",           
            'vacation_hours',
            'sick_hours',
            'other_hours',
            'holiday_hours',
         
        ]

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)        
        self.fields['date'].disabled = True
        self.fields['EmployeeID'].disabled = True
        self.fields['periodID'].disabled = True
        self.fields['regular_hours'].widget.attrs['readonly'] = True

class wtcSupForm(forms.ModelForm):      
    

    class Meta:
        model = paidBySalary
        fields = [   
            'EmployeeID',  
            'periodID',
            'date',        
            "regular_hours",           
            'vacation_hours',
            'sick_hours',
            'other_hours',
            'holiday_hours',
          
        ]

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)        
        self.fields['date'].required = True
        self.fields['EmployeeID'].disabled = True
        self.fields['periodID'].disabled = True
        self.fields['regular_hours'].widget.attrs['readonly'] = True
        

class bthForm(forms.ModelForm):

    class Meta:
        model = paidByTheHour
        fields= [
            'EmployeeID',  
            'date',
            'clockIn' ,
            'clockOut' ,
            'breakIn' ,
            'breakOut' ,
            'lunchIn' ,
            'lunchOut' ,
            'total_hours' ,
            'regular_hours' ,
            'overtime_hours' ,
            'double_time' ,
            'vacation_hours' ,
            'sick_hours',
            'holiday_hours' ,
            'other_hours',
        ]

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)        
        self.fields['date'].required = True
        self.fields['EmployeeID'].disabled = True


class paidByHourManually_Form(forms.ModelForm):      
    

    class Meta:
        model = paidByHourManually
        fields = [   
            'EmployeeID',  
            'periodID',
            'date',        
            "total_hours",           
            'overtime_hours',
            'regular_hours',
            'double_time',
            'comments'
        ]

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)        
        self.fields['date'].disabled = True
        self.fields['EmployeeID'].disabled = True
        self.fields['periodID'].disabled = True
        self.fields['regular_hours'].widget.attrs['readonly'] = True
        self.fields['overtime_hours'].widget.attrs['readonly'] = True
        self.fields['double_time'].widget.attrs['readonly'] = True


class paidByHourManuallySup_Form(forms.ModelForm):      
    
    class Meta:
        model = paidByHourManually
        fields = [   
            'EmployeeID',  
            'periodID',
            'date',        
            "total_hours",    
            "regular_hours",       
            'overtime_hours',
            'double_time',
            'comments'
        ]

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)        
        self.fields['date'].required = True
        self.fields['EmployeeID'].disabled = True
        self.fields['periodID'].disabled = True