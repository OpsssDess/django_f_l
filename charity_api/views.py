from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from charity.models import *
from charity_api.serializes import ThingSerializer


class ThingAPI(APIView):
    def get(self, request, format=None):

        things = [ThingSerializer(thing).data for thing in Thing.objects.all()]
        return Response(things)

