import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import transaction, IntegrityError
from django.db.models import Q, F

from charity.forms import *


def index(request):
    button_disabled = False
    if request.session.get('office_id'):
        office = Office.objects.get(id=request.session['office_id'])
        button_disabled = office.ocupied >= office.capacity

    context = {
        'form': DonateForm(),
        'officeForm': OfficeForm(),
        'button_disabled': button_disabled,
    }
    return render(request, 'charity/index.html', context)


@transaction.atomic()
def donate(request):
    if request.method == 'POST':
        form = DonateForm(request.POST)
        if form.is_valid():
            Good = form.save(commit=False)
            Good.office = Office.objects.select_for_update().get(id=request.session['office_id'])
            if Good.office.capacity > Good.amount + Good.office.ocupied:
                Good.save()
                form.save_m2m()
            else:
                form.add_error(Good.amount, 'слишком большое количество вещей!')
    return redirect('main')

def ask_good(request):
    availability = Thing.objects.all().exists()
    if availability:
        last_good = Thing.objects.order_by('-pk')[0]
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

def add_request(request):
    context = {
        'move': request.POST.get('move'),
        'N': request.POST.get('num'),
    }
    return render(request, 'charity/add_request.html', context)

def req_or_donate(request):
    print(request.POST['move'])

    if request.method == 'POST':
        if request.POST['move'] == 'request':
            for i in range(int(request.POST['amount'])):
                Thing.objects.create(name=request.POST[f'name_{i+1}'], category_id=1)
                print(request.POST[f'name_{i+1}'])
            unic = HelpRequest.objects.create()
        else:
            unic = Donation.objects.create()
    context = {
        'unic': unic.donation_hash,
    }
    return render(request, 'charity/tnx.html', context)
