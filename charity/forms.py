from django import forms
from charity.models import *

class DonateForm(forms.ModelForm):
    class Meta:
        model = Thing
        exclude = ['office']

class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['address']

class OfficeFormChoise(forms.Form):
    officeChoise = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        widget=forms.Select(attrs={"onChange": 'form.submit();'}),
    )

class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ['name',]

