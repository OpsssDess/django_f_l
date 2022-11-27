from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from rest_framework import routers

from .views import *

app_name = 'charity_api'

donation_item_router = routers.DefaultRouter()
donation_item_router.register(r'donationitem', DonationItemViewSet)

item_description_router = routers.DefaultRouter()
item_description_router.register(r'itemdescription', ItemDescriptionViewset)

request_item_router = routers.DefaultRouter()
request_item_router.register(r'requestitem', ShowRequestItemViewset, basename='requestitem')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('charity-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('things/', views.ThingAPIList.as_view()),
    path('things/<int:pk>/', views.ThingAPIUpdate.as_view()),
    path('thingsdelete/<int:pk>/', views.ThingAPIDestroy.as_view()),

    path('', include(donation_item_router.urls)),
    path('', include(item_description_router.urls)),
    path('', include(request_item_router.urls)),

]