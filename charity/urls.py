from django.urls import path

from charity.views import *

urlpatterns = [
    path('', index, name='main'),
    path('set_session_office', set_session_office, name='set_session_office'),
    path('donate', donate),

    path('login', login, name='login'),

    path('register', RegisterUser.as_view(), name='register'),

    path('completed_request', CompletedRequestView.as_view(), name='completed_request_list'),
    path('add_request_donate', add_request_donate),
    path('list_donation', list_donation),
    path('processing_request_item', processing_request_item),
    path('change_request_status', change_request_status),
    path('add_description', add_description),
    ]