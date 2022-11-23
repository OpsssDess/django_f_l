from django.urls import path

from charity.views import *

urlpatterns = [
    path('', index, name='main'),
    path('set_session_office', set_session_office, name='set_session_office'),
    path('donate2', donate2),
    path('choice_move', choice_move),
    path('help_request', help_request),


    path('get_item', get_item),

    path('HomePageView', HomePageView.as_view(), name='home_page'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('register', RegisterUser.as_view(), name='register'),

    path('completed_request', RequestItemView.as_view(), name='completed_request_list'),
    path('list_donation', list_donation),
    # path('change_request_status', change_request_status),
    path('add_description', add_description),
]
