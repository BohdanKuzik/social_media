from django.contrib import admin

from users.models import Profile, Follow


admin.site.register(Profile)
admin.site.register(Follow)
