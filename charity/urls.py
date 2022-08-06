from django.urls import path

from charity.views import *

urlpatterns = [
    path('', index),
    path('donate', donate),
    path('ask_good', ask_good),
]