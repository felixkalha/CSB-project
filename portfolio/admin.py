from django.contrib import admin

from .models import Comment, Project

admin.site.register(Project)
admin.site.register(Comment)