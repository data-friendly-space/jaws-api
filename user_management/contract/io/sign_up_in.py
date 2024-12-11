"""Request object to create an analysis contract"""
from rest_framework import serializers


class SignUpIn(serializers.Serializer):
    name = serializers.CharField(max_length=60)
    lastname = serializers.CharField(max_length=60)
    email = serializers.CharField(max_length=120)
    password = serializers.CharField(max_length=20)
