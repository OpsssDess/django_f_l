import json

from django.shortcuts import render
from django.http import HttpResponse

from charity.forms import *

stock = []
form = DonateForm()

def index(request):
    return render(request, 'charity/index.html', {'form': form})

def donate(request):
    Good.objects.create(name_good=request.POST['good'], amount=request.POST['amount'])
    return render(request, 'charity/request_donation.html')

def ask_good(request):
    availability = Good.objects.all().exists()

    if availability:
        last_good = Good.objects.order_by('-time_create')[0]
        # or last_good = Good.objects.last()
        last_good.amount -= 1
        last_good.save()
        if last_good.amount == 0:
            last_good.delete()
        context = {'availability': availability, 'take_good': last_good.name_good}
        return render(request, 'charity/request_take.html', context)
    else:
        return render(request, 'charity/request_take.html')