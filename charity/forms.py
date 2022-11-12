from django import forms
from django.forms import formset_factory, BaseModelFormSet, modelformset_factory, Textarea
from charity.models import *


class ThingForm(forms.ModelForm):
    class Meta:
        model = Thing
        fields = ['name', 'type_thing', 'category', 'amount']

class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['address']

class OfficeFormChoise(forms.Form):
    officeChoise = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        widget=forms.Select(attrs={"onChange": 'form.submit();'}),
    )


class ItemFormChoise(forms.Form):
    thing_choice = forms.ModelChoiceField(queryset=Thing.objects.all())
    amount = forms.IntegerField()


class ItemDescriptionForm(forms.ModelForm):
    class Meta:
        model = ItemDescription
        fields = ['details', 'name', 'condition', 'base_item_hash', 'office', 'image']

