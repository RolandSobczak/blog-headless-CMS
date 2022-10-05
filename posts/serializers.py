from django.urls import reverse_lazy
from rest_framework import serializers
from .models import Post, File, Comment, Tags, Like


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        # fields['comments_url'] = None
        return fields

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'