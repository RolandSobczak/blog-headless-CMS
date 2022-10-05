from django.urls import path, include
from rest_framework import routers
from .views import NewsletterViewSet, MailViewSet

router = routers.DefaultRouter()
router.register('mail', MailViewSet, "mail")
router.register('', NewsletterViewSet, "newsletter")

app_name = 'mails'

urlpatterns = [
    path('', include(router.urls)),
]