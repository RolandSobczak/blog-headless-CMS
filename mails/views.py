from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Newsletter, Mail
from .serializers import NewsletterSerializer, MailSerializer


class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = (IsAdminUser,)


    @action(detail=False, methods=['post', 'delete', 'get'], permission_classes=(AllowAny,))
    def follow(self, request, *args, **kwargs):
        email_query = Newsletter.objects.filter(mail=request.user.email)
        serializer = self.get_serializer(data=request.data)
        if request.method == 'GET':
            return Response(
                {"status": True if email_query.exists() else False},
                status=200
            )
        if email_query.exists():
            if request.method == 'POST':
                return Response({'error': 'This email already in newsletter'}, status=403)
            email_query.first.delete()
            return Response({'status': False}, status=200)
        if request.method == 'DELETE':
            return Response({'error': 'This email is not in the newsletter'}, status=403)
        if serializer.is_valid():
            Newsletter.objects.create(mail=serializer.validated_data["mail"], is_active=False)
            return Response({'status': True}, status=201)
        return Response({"errors": serializer.errors}, status=403)


class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    permission_classes = (IsAdminUser,)

