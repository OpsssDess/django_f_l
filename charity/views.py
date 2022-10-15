import json

from django.shortcuts import render, redirect
from django.http import HttpResponse

from charity.forms import *

stock = []

def index(request):
    context = {
        'form': DonateForm(),
        'officeForm': OfficeForm(),
    }
    return render(request, 'charity/index.html', context)

def donate(request):
    if request.method == 'POST':
        form = DonateForm(request.POST)
        if form.is_valid():
            Good = form.save(commit=False)
            Good.office_id = request.session['office_id']
            Good.save()
            form.save_m2m()
    return render(request, 'charity/request_donation.html')

def ask_good(request):
    availability = Good.objects.all().exists()
    if availability:
        last_good = Good.objects.order_by('-stock','-time_create')[0]
        last_good.amount -= 1
        last_good.save()
        if last_good.amount == 0:
            last_good.delete()
        context = {'availability': availability, 'take_good': last_good.thing}
        return render(request, 'charity/request_take.html', context)
    else:
        return render(request, 'charity/request_take.html')

def set_session_office(request):
    form = OfficeFormChoise(data=request.POST)
    if form.is_valid():
        request.session['office_id'] = form.cleaned_data['officeChoise'].id
    return redirect('main')