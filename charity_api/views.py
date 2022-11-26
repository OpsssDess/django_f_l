from rest_framework import generics
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import *
from charity.models import *
from charity_api.permissions import IsAdminOrReadOnly, IsOwnderOrReadOnly
from charity_api.serializes import ThingSerializer

class ThingAPIListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class ThingAPIList(generics.ListCreateAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = ThingAPIListPagination


class ThingAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = (IsOwnderOrReadOnly, )


class ThingAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (TokenAuthentication, )


