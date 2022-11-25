from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from charity.models import *
from charity_api.serializes import ThingSerializer


class ThingAPIList(generics.ListCreateAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer

class ThingAPIUpdate(generics.UpdateAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer

class ThingAPIDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer


