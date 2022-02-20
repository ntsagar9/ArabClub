from django.contrib import admin

from newsfeed.models import Post, Tag


class Tags(admin.TabularInline):
    model = Tag





admin.site.register(Tag)
admin.site.register(Post)
# Register your models here.
