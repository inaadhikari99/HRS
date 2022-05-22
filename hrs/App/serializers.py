from ast import keyword
from turtle import title
from rest_framework import serializers
from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    price = serializers.IntegerField()
    location = serializers.CharField()
    cuisine = serializers.CharField()

    class Meta:
        model = Hotel
        fields = ('id', 'name', 'price', 'location', 'cuisine')
