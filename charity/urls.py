from django.urls import path

from charity.views import *

urlpatterns = [
    path('', index, name='main'),
    path('create_donate_or_help', create_donate_or_help, name='create_donate_or_help'),
    path('donate2', donate2),
    path('create_help_request', create_help_request),

    path('set_session_office', set_session_office, name='set_session_office'),
    path('donate', donate),

    path('login', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('register', RegisterUser.as_view(), name='register'),

    path('completed_request', CompletedRequestView.as_view(), name='completed_request_list'),
    path('add_request_donate', add_request_donate),
    path('list_donation', list_donation),
    path('processing_request_item', processing_request_item),
    path('change_request_status', change_request_status),
    path('add_description', add_description),
    ]