from django.urls import path, re_path
from . import views

app_name = 'charity_api'

urlpatterns = [
    path('things', views.ThingAPI.as_view())
]