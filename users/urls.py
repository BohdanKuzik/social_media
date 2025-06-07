from django.urls import path

from users.views import CreateUserView, LoginUserView, ManageUserView


app_name = "users"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", LoginUserView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="manage_user"),
]
