from django import forms
from charity.models import *

class DonateForm(forms.Form):
    thing = forms.CharField(label = 'Какую вещь хотите отдать?', max_length=255)
    amount = forms.IntegerField(min_value=0, label='количество')
    stock = forms.CharField(max_length=255, label='сортировка')
    state = forms.CharField(max_length=255, label='состояние')
    office = forms.ModelChoiceField(queryset=Office.objects.all(), label='офис')