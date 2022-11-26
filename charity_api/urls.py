from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = 'charity_api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('charity-auth/', include('rest_framework.urls')),
    path('things/', views.ThingAPIList.as_view()),
    path('things/<int:pk>/', views.ThingAPIUpdate.as_view()),
    path('thingsdelete/<int:pk>/', views.ThingAPIDestroy.as_view()),

]