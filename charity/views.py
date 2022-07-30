import json

from django.shortcuts import render
from django.http import HttpResponse

from forms import *

stock = []
form = DonateForm()

def index(request):
    return render(request, 'charity/index.html', {'form': form})



def donate(request):
    print(request.POST)
    if request.POST['f_or_l'] == 'LIFO':
        stock.append({"name": request.POST['good'], "amount": request.POST['amount']})
    else:
        stock.insert(0, {"name": request.POST['good'], "amount": request.POST['amount']})
    print(stock)
    with open('good', 'w', encoding='utf-8') as f:
        json.dump(stock, f)
    return render(request, 'charity/request_donation.html')

def ask_good(request):
    with open('good', mode="r", encoding='utf-8') as file:
        stock1 = json.load(file)

    donation = {}

    if stock1:
        last_thing = stock1[len(stock1) - 1]
        if int(last_thing['amount']) == 1:
            donation = stock1.pop()
        else:
            one_time_var = int(last_thing['amount'])
            last_thing['amount'] = one_time_var - 1
            donation = stock1[-1]

        with open('good', 'w', encoding='utf-8') as f:
            json.dump(stock1, f)

        context = {'take_good': donation['name']}

        return render(request, 'charity/request_take.html', context)
    else:
        return render(request, 'charity/request_take.html')
