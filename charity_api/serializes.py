from rest_framework import serializers

from charity.models import *


class ThingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Thing
        fields = "__all__"


class ItemDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemDescription
        fields = "__all__"


class DonationItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = DonationItem
        fields = "__all__"