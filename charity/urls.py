from django.urls import path

from charity.views import *

urlpatterns = [
    path('', index, name='main'),
    path('set_session_office', set_session_office, name='set_session_office'),
    path('donate', donate),
    path('choice_move', choice_move),
    path('help_request', help_request),

    path('login', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('register', RegisterUser.as_view(), name='register'),
    path('search', Search.as_view(), name='search'),

    path('requests', RequestItemView.as_view(), name='request_list'),
    path('donations', list_donation, name='list_donation'),
]
