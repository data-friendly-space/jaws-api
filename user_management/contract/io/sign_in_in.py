"""Request object to create an analysis contract"""
from rest_framework import serializers


class SignInIn(serializers.Serializer):
    email = serializers.CharField(max_length=120)
    password = serializers.CharField(max_length=20)
