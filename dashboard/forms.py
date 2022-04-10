from django import forms
from .models import FoodAcceptor

class FoodRequestForm(forms.ModelForm):
    
    class Meta:
        model = FoodAcceptor
        fields = ['contact_number', 'any_message']
