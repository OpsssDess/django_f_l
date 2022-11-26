from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import *
from charity.models import *
from charity_api.permissions import IsAdminOrReadOnly, IsOwnderOrReadOnly
from charity_api.serializes import ThingSerializer


class ThingAPIList(generics.ListCreateAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class ThingAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = (IsOwnderOrReadOnly, )

class ThingAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = (IsAdminOrReadOnly,)


