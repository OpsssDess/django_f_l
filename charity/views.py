from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.db import transaction, IntegrityError
from django.forms import formset_factory, modelformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

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
        'form_d': ItemDescriptionForm(),
    }
    return render(request, 'charity/index.html', context)


@transaction.atomic()
def donate(request):
    actual_office = Office.objects.get(id=request.session['office_id'])
    donation = Donation.objects.create()
    context = {
        'unic': donation.donation_hash,
        'label': False,
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


def set_session_office(request):
    form = OfficeFormChoise(data=request.POST)
    if form.is_valid():
        request.session['office_id'] = form.cleaned_data['officeChoise'].id
    return redirect('main')


def add_request_donate(request):
    count_things = request.POST.get('num')
    context = {
        'form': ItemFormChoise,
        'N': count_things,
    }
    return render(request, 'charity/add_request.html', context)


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
        'unic': help_request.donation_hash,
        'label': True,
    }
    return render(request, 'charity/tnx.html', context)


@transaction.atomic()
def change_request_status(request):
    hash = request.GET['hash']

    help_request = HelpRequest.objects.get(donation_hash=uuid.UUID(hash))
    help_request.status_help_request = 'satisfied'
    help_request.save()

    req_item = RequestItem.objects.get(request_id=help_request.pk)

    good = Thing.objects.get(pk=req_item.base_item_hash_id)
    good.amount -= 1
    good.save()

    donation_item = DonationItem.objects.get(base_item_hash=good.pk)

    donation = Donation.objects.get(pk=donation_item.donation_id)
    donation.status_donation = 'booked'
    donation.save()

    context = {
        'good': good,
    }
    return render(request, 'charity/end.html', context)


def list_donation(request):
    don_list = DonationItem.objects.all()
    paginator = Paginator(don_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj,}
    return render(request, 'charity/list_donations.html', context)

'''добавить корректную ссылку на донат в итем'''
def add_description(request):
    donate_item = DonationItem.objects.get()
    actual_office = Office.objects.get(id=request.session['office_id'])
    donation = Donation.objects.create()
    context = {
        'unic': donation.donation_hash,
        'label': False,
    }
    if request.method == 'POST':
        form = ItemDescriptionForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.donation_id = donation.pk
            item.save()
            form.save_m2m()

    return render(request, 'charity/tnx.html', context)

class CompletedRequestView(ListView):
    template_name = 'charity/request_list.html'
    model = RequestItem
    context_object_name = 'requests'
    paginate_by = 10

def login(request):
    return redirect('main')

class RegisterUser(CreateView):
    form_class = RegUserForm
    template_name = 'charity/register.html'
    success_url = reverse_lazy('login')
