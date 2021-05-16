from rest_framework import serializers

from customer.models import Customer


class CustomerLocationSerializer(serializers.ModelSerializer):

    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'name',
            'latitude',
            'longitude',
        )

    def get_latitude(self, obj):
        return obj.location[0]

    def get_longitude(self, obj):
        return obj.location[1]
