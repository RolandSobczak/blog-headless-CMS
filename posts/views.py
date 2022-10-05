from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment, File, Tags, Like
from .serializers import PostsSerializer, CommentSerializer, FileSerializer, TagsSerializer, LikeSerializer
from .filters import IsAdminFilterBackend
from utils.permissions import IsAuthor, IsAdminOrReadOnly
from rest_framework import authentication


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IsAdminFilterBackend(active=True), DjangoFilterBackend,)


    @action(detail=True,
            methods=['post', 'delete', 'get',],
            permission_classes=(IsAuthenticated,))
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        like_query = Like.objects.filter(post=post, user=request.user)
        if request.method == 'GET':
           return Response(
               {"status": True if like_query.exists() else False},
               status=200
           )
        if like_query.exists():
            if request.method == 'POST':
                return Response({'error': 'This user already likes this post'}, status=403)
            like_query.delete()
            return Response({'post_url': post.get_absolute_url()}, status=200)
        if request.method == 'DELETE':
            return Response({'error': 'This user doesn\'t like this post'}, status=403)
        Like.objects.create(post=post, user=request.user)
        return Response({'post_url': post.get_absolute_url()}, status=201)



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthor(admin_methods=('POST', 'DELETE',)))


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IsAdminFilterBackend(post__active=True), DjangoFilterBackend,)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAdminOrReadOnly,)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAdminOrReadOnly,)
