from django.urls import path, re_path
from . import views

app_name = 'charity_api'

urlpatterns = [
    path('things/', views.ThingAPIList.as_view()),
    path('things/<int:pk>/', views.ThingAPIUpdate.as_view()),
    path('thingsdetail/<int:pk>/', views.ThingAPIDetails.as_view()),

]