from django.contrib import admin

from newsfeed.models import Post
from tag_system.models import Tag


class Tags(admin.TabularInline):
    model = Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Tag)
admin.site.register(Post, PostAdmin)