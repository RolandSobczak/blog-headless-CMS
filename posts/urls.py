from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet, CommentViewSet, FileViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet, "posts")
router.register('comments', CommentViewSet, "comments")
router.register('files', FileViewSet, "files")

app_name = 'posts'

urlpatterns = [
    path('', include(router.urls)),
]