from django.contrib import admin

from newsfeed.models import Post, Tag, Comments, Reply


class Tags(admin.TabularInline):
    model = Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comments)
admin.site.register(Reply)
# Register your models here.
