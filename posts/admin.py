from django.contrib import admin

from posts.models import Post, Like, Comment, Hashtag

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Hashtag)
