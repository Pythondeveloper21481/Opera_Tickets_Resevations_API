# this file is  responsibale of the transformations of our data to JSON code

from rest_framework import serializers
from tickets.models import Guest, Opera, Post, Reservation

class OperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opera
        fields = '__all__'


class ResevationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk', 'reservation', 'name', 'mobile']

class PostSerializer(serializers.ModelSerializer):
     class Meta:
        model = Post
        fields = '__all__'