from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.text import slugify
from utils.fields import HTMLField
from utils.models import Timestamped


class ActivePostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Tags(models.Model):
    slug = models.SlugField(max_length=36)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        return super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=72, unique=True, blank=True)
    img = models.ImageField(upload_to='category/img/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)
        return super().save(*args, **kwargs)

class Post(Timestamped):
    active = models.BooleanField(default=False)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=240, unique=True)
    content = HTMLField()
    img = models.ImageField(upload_to='posts/img/')
    tags = models.ManyToManyField(Tags, related_name='posts', null=True)
    category = models.ForeignKey(Category, related_name='posts', null=True, on_delete=models.DO_NOTHING)

    objects = models.Manager()
    actives = ActivePostsManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('posts:posts-detail', kwargs={'pk': self.id})

class File(models.Model):
    post = models.ForeignKey(Post, related_name='files', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = models.FileField(upload_to='posts/files/')


class Comment(Timestamped):
    author = models.ForeignKey(get_user_model(), related_name='comments', on_delete=models.CASCADE)
    content = HTMLField()
    answer = models.PositiveIntegerField(null=True)


class Like(Timestamped):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name='likes', on_delete=models.CASCADE)


