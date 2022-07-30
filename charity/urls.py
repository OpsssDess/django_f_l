from django.urls import path

from views import *

urlpatterns = [
    path('', index),
    path('donate', donate),
    path('ask_good', ask_good),
]