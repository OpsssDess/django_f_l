from django.urls import path

from charity.views import *

urlpatterns = [
    path('', index, name='main'),
    path('set_session_office', set_session_office, name='set_session_office'),
    path('donate', donate),
    path('ask_good', ask_good),
    path('add_request', add_request),
    path('register_request', register_request),
    ]