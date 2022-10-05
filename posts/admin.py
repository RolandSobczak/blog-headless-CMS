from django.contrib import admin
from .models import Post, File

@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    pass


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass