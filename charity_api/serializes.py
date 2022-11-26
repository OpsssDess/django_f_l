from rest_framework import serializers

from charity.models import Thing


class ThingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Thing
        fields = "__all__"
