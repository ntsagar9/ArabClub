from django.contrib import admin

from comments_system.models import Comment, Reply

admin.site.register(Reply)
admin.site.register(Comment)
# Register your models here.
