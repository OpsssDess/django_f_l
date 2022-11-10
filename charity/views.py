from django.shortcuts import render, redirect
from django.db import transaction, IntegrityError
from django.forms import formset_factory, modelformset_factory

from charity.forms import *


def index(request):
    button_disabled = False
    if request.session.get('office_id'):
        office = Office.objects.get(id=request.session['office_id'])
        button_disabled = office.ocupied >= office.capacity

    context = {
        'form': ThingForm(),
        'officeForm': OfficeForm(),
        'button_disabled': button_disabled,
    }
    return render(request, 'charity/index.html', context)


@transaction.atomic()
def donate(request):
    actual_office = Office.objects.get(id=request.session['office_id'])
    donation = Donation.objects.create()
    context = {
        'unic': donation.donation_hash
    }
    if request.method == 'POST':
        form = ThingForm(request.POST)
        if form.is_valid():
            thing = form.save()
            DonationItem.objects.create(
                donation_id=donation.id,
                base_item_hash_id=thing.pk,
                office_id=actual_office.pk
            )
    return render(request, 'charity/tnx.html', context)


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

def add_request_donate(request):
    count_things = request.POST.get('num')
    print(request.POST['move'])
    if request.POST['move'] == 'donate':
        move = ThingForm()
        link = 'donate'
    else:
        move = ItemFormChoise()
        link = 'request'
    context = {
        'link': link,
        'form': move,
        'N': count_things,
    }
    return render(request, 'charity/add_request.html', context)

def create_donate(request):
    actual_office = Office.objects.get(id=request.session['office_id'])
    donation = Donation.objects.create()
    if request.method == 'POST':
        form = ThingForm(request.POST)
        if form.is_valid():
            thing = form.save()
            DonationItem.objects.create(
                donation_id=donation.id,
                base_item_hash=Thing.objects.get(id=thing.id),
                office_id=actual_office.pk
                )
    context = {
        'unic': donation.donation_hash
    }
    return render(request, 'charity/tnx.html', context)



def processing_request_item(request):
    actual_office = Office.objects.get(id=request.session['office_id'])
    help_request = HelpRequest.objects.create()
    if request.method == 'POST':
        req_thing = Thing.objects.get(pk=request.POST['thing_choice'])
        RequestItem.objects.create(
            office_id=actual_office.pk,
            base_item_hash_id=req_thing.pk,
            request_id=help_request.id
        )
    context = {
        'unic': help_request.donation_hash
    }
    return render(request, 'charity/tnx.html', context)


def list_donation(request):
    context = {'data': DonationItem.objects.all()}
    return render(request, 'charity/list_donations.html', context)
