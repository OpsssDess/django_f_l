from django import forms
from charity.models import *

class DonateForm(forms.ModelForm):
    class Meta:
        model = Good
        exclude = ['office']
    # thing = forms.CharField(label = 'Какую вещь хотите отдать?', max_length=255)
    # amount = forms.IntegerField(min_value=0, label='количество')
    # stock = forms.CharField(max_length=255, label='сортировка')
    # state = forms.CharField(max_length=255, label='состояние')
    # office = forms.ModelChoiceField(queryset=Office.objects.all(), label='офис')

class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['address']

class OfficeFormChoise(forms.Form):
    officeChoise = forms.ModelChoiceField(
        queryset=Office.objects.all()
    )

