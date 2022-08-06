from django import forms
from charity.models import *

class DonateForm(forms.Form):
    good = forms.CharField(label = 'Какую вещь хотите отдать?', max_length=255)
    amount = forms.IntegerField(min_value=0)
    f_or_l = forms.CharField(max_length=255)

