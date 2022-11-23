from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse
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
        'button_disabled': button_disabled,
        'form_d': ItemDescriptionForm(),
    }
    return render(request, 'charity/index.html', context)

def choice_move(request):
    if request.method == 'POST':
        if request.POST['question'] == 'donate':
            donate = Donation.objects.create()
            context = {
                'unic': donate.donation_hash,
                'form_d': ItemDescriptionForm(),
            }
            return render(request, 'charity/donate.html', context)
        else:
            help_request = HelpRequest.objects.create()
            context = {
                'unic': help_request.donation_hash,
                'form': RequestItemForm()
            }
            return render(request, 'charity/help_request.html', context)

@transaction.atomic()
def donate2(request):
    donate = Donation.objects.order_by('-creation_date')[0]
    actual_office = Office.objects.get(id=request.session['office_id'])
    context = {'unic': donate.donation_hash}
    if request.method == 'POST':
        form = ItemDescriptionForm(data=request.POST)
        if form.is_valid():
            new_don_item = form.save(commit=False)
            new_don_item.donation_id = donate.pk
            new_don_item.office_id = actual_office.pk
            new_don_item.save()
            form.save_m2m()

    return render(request, 'charity/tnx.html', context)

def get_item(request):
    donate = Donation.objects.order_by('-creation_date')[0]
    # actual_office = Office.objects.get(id=request.session['office_id'])
    context = {'unic': donate.donation_hash}
    if request.method == 'POST':
        form = ItemDescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            # item.image = request.FILES['image']
            item.save()
            # form.save_m2m

    return render(request, 'charity/tnx.html', context)

class HomePageView(ListView):
    model = ItemDescription
    template_name = 'charity/descriptions.html'

def help_request(request):
    help_req = HelpRequest.objects.order_by('-creation_date')[0]
    actual_office = Office.objects.get(id=request.session['office_id'])
    context = {
        'unic': help_req.donation_hash,
        'label': False,
    }
    if request.method == 'POST':
        form = RequestItemForm(data=request.POST)
        if form.is_valid():
            r_item = form.save(commit=False)
            r_item.request_id = help_req.pk
            r_item.office_id = actual_office.pk
            r_item.save()
            form.save_m2m()

    return render(request, 'charity/tnx.html', context)


def set_session_office(request):
    form = OfficeFormChoise(data=request.POST)
    if form.is_valid():
        request.session['office_id'] = form.cleaned_data['officeChoise'].id
    return redirect('main')


# @transaction.atomic()
# def change_request_status(request):
#     hash = request.GET['hash']
#
#     help_request = HelpRequest.objects.get(donation_hash=uuid.UUID(hash))
#     req_item = RequestItem.objects.get(request_id=help_request.pk)
#     need_good = req_item.base_item_hash
#     need_don_item = DonationItem.objects.get(base_item_hash__exact=need_good)
#     if need_don_item:
#         help_request.status_help_request = 'satisfied'
#         help_request.save()
#
#         need_don_item.donation.status_donation = 'booked'
#         need_don_item.save()
#     else:
#         return HttpResponse("Ваш запрос не удовлетворён, подождите!")
#
#     context = {
#         'good': need_good,
#     }
#     return render(request, 'charity/end.html', context)


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

class RequestItemView(ListView):
    template_name = 'charity/request_list.html'
    model = RequestItem
    context_object_name = 'requests'
    paginate_by = 10


class RegisterUser(CreateView):
    form_class = RegUserForm
    template_name = 'charity/register.html'
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'charity/login.html'

    def get_success_url(self):
        return reverse_lazy('main')

def logout_user(request):
    logout(request)
    return redirect('login')