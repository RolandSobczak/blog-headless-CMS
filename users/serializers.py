from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Profile
from djoser import serializers as djoser_serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('image', 'description',)


class UserSerializer(djoser_serializers.UserSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

    profile = ProfileSerializer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context['request'].user.is_staff:
            self.Meta.fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'profile')
            if not isinstance(self.instance, get_user_model()) or not self.context['request'].user.is_authenticated:
                self.Meta.fields = ('pk', 'username', 'profile')



class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()


class ActivationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    uidb64 = serializers.CharField()
