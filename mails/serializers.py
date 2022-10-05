from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Newsletter, Mail
from utils.validators import ObjectExistsValidator


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

    is_active = serializers.BooleanField(required=False)


class MailSerializer(serializers.ModelSerializer):
    # newsletters = serializers.ListField(
    #     child=serializers.IntegerField(min_value=1)
    # )
    newsletters = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=Newsletter.objects.all())
    users = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=get_user_model().objects.all())

    class Meta:
        model = Mail
        fields = '__all__'


    def create(self, validated_data):
        newsletters = None
        users = None
        if validated_data.get('newsletters'):
            newsletters = validated_data.pop('newsletters')
        if validated_data.get('users'):
            users = validated_data.pop('users')
        mail = Mail.objects.create(**validated_data)
        if newsletters:
            mail.newsletters.set(newsletters)
        if users:
            mail.users.set(users)
        return mail


