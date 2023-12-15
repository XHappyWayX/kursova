from rest_framework import serializers
from .models import Resource, CustomUser


class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user