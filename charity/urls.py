from django.urls import path

from charity.views import *

urlpatterns = [
    path('', index, name='main'),
    path('set_session_office', set_session_office, name='set_session_office'),
    path('donate', donate),
    path('ask_good', ask_good),
    path('add_request_donate', add_request_donate),
    path('create_donate', create_donate),
    path('list_donation', list_donation),
    path('processing_request_item', processing_request_item)
    ]