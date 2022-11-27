from rest_framework import generics, mixins
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from charity.models import *
from charity_api.permissions import IsAdminOrReadOnly, IsOwnderOrReadOnly
from charity_api.serializes import *

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


class ItemDescriptionViewset(viewsets.ModelViewSet):
    queryset = ItemDescription.objects.all()
    serializer_class = ItemDescriptionSerializer

    @action(methods=['get', 'post'], detail=True)
    def show_donationitem(self, request, pk=None):
        don_item = DonationItem.objects.get(pk=pk)
        return Response({'donationitems': don_item.base_item_hash.name,
                         'donation_id': don_item.donation_id,
                         })

class DonationItemViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = DonationItem.objects.all()
    serializer_class = DonationItemSerializer


class ShowRequestItemViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = RequestItemSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if not pk:
            return RequestItem.objects.all()
        return RequestItem.objects.filter(pk=pk)

