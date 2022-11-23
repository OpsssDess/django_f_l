from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import formset_factory, BaseModelFormSet, modelformset_factory, Textarea
from charity.models import *

class DonationItemForm(forms.ModelForm):
    class Meta:
        model = DonationItem
        exclude = ['donation', 'office']


class RequestItemForm(forms.ModelForm):
    class Meta:
        model = RequestItem
        exclude = ['request', 'office']


class OfficeFormChoise(forms.Form):
    officeChoise = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        label='склад',
        widget=forms.Select(attrs={"onChange": 'form.submit();'}),
    )


class ItemDescriptionForm(forms.ModelForm):
    class Meta:
        model = ItemDescription
        exclude = ['donation', 'office', ]


class RegUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=("Используйте сложный пароль"),
    )
    password2 = forms.CharField(
        label=("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=("Введите пароль ещё раз"),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)




