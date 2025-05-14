from rest_framework import serializers

class InstrumentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    description = serializers.CharField(allow_blank=True, required=False)
