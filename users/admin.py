from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from posts.models import Follow, Profile
from users.models import CustomUser as User


admin.site.register(
    User,
    UserAdmin,
)
admin.site.register(Profile)
admin.site.register(Follow)
