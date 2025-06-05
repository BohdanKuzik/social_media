from rest_framework import routers

from posts.views import (
    PostViewSet,
    CommentViewSet,
    FollowViewSet,
    ProfileViewSet,
    LikeViewSet,
    HashtagViewSet,
)

app_name = "social_media"

router = routers.DefaultRouter()

router.register("profiles", ProfileViewSet)
router.register("follows", FollowViewSet)
router.register("posts", PostViewSet)
router.register("likes", LikeViewSet)
router.register("comments", CommentViewSet)
router.register("hashtags", HashtagViewSet)


urlpatterns = router.urls
