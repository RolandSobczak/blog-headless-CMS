from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from . import serializers
from .token import account_activation_token
from .tasks import send_activation_email
from utils.permissions import IsAuthor


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserPublicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthor(attr=''))

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return serializers.UserAdminSerializer
        elif self.request.user == self.get_object():
            return serializers.UserPrivateSerializer
        return serializers.UserPublicSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        user = User.objects.get(username=username)
        activation_page = serializer.validated_data["activation_page"]
        send_activation_email.delay()
        return response



class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = serializers.TokenSerializer
    permission_classes = (IsAdminUser,)

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user_query = User.objects.filter(Q(username=username) | Q(email=username))
            if user_query.exists():
                user = user_query.first()
                if user.check_password(password):
                    return Response(
                        {
                            "token": Token.objects.get_or_create(user=user)[0].key,
                            "user_url": user.get_absolute_url(),
                        },
                        status=status.HTTP_200_OK
                    )
            return Response({"error": "Invalid password or username"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors)


class AccountActivationView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ActivationTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data.get("uidb64")
            token = serializer.validated_data.get("token")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {'user_url': user.get_absolute_url(), 'token': reverse_lazy("users:login")},
                status=status.HTTP_200_OK
            )
        return Response({'error': "Invalid/Inactive token or uidb64"}, status=status.HTTP_403_FORBIDDEN)



