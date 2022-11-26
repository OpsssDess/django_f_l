from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from rest_framework import routers

from .views import *

app_name = 'charity_api'

donation_item_router = routers.SimpleRouter()
donation_item_router.register(r'donationitem', DonationItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('charity-auth/', include('rest_framework.urls')),

    path('things/', views.ThingAPIList.as_view()),
    path('things/<int:pk>/', views.ThingAPIUpdate.as_view()),
    path('thingsdelete/<int:pk>/', views.ThingAPIDestroy.as_view()),

    path('itemdescription/', views.ItemDescriptionAPIList.as_view()),
    path('', include(donation_item_router.urls)),
    # path('donationitem/', views.DonationItemViewSet.as_view({'get': 'list'})),
    # path('donationitem/<int:pk>/', views.DonationItemViewSet.as_view({'get': 'retrieve'})),

    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]