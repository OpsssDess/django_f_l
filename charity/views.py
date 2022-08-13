import json

from django.shortcuts import render, redirect
from django.http import HttpResponse

from charity.forms import *

stock = []


def index(request):
    form = DonateForm()
    return render(request, 'charity/index.html', {'form': form})

def donate(request):
    if request.method == 'POST':
        form = DonateForm(request.POST)
        if form.is_valid():
            try:
                Good.objects.create(**form.cleaned_data)
                return redirect('')
            except:
                form.add_error(None, 'Ошибка добавления вещи')

        else:
            form = DonateForm()
    # if "office" in request.session:
    #     result = request.session["office"]
    # else:
    #     result = request.POST['office']
    # Good.objects.create(thing=request.POST['thing'], amount=request.POST['amount'], stock=request.POST['stock'], office=request.POST['office'])
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