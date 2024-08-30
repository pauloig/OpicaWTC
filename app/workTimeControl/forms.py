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
        ]

    def __init__(self, *args, **kwargs):        
        super().__init__(*args, **kwargs)        
        self.fields['date'].disabled = True
        self.fields['EmployeeID'].disabled = True
        self.fields['periodID'].disabled = True
        