from rest_framework import serializers

class ThingSerializer(serializers.Serializer):
    name = serializers.CharField()
    type_thing = serializers.CharField()
    category = serializers.CharField()