from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from posts.models import Post, Comment, Profile, Like, Follow, Hashtag
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
    FollowSerializer,
    HashtagSerializer,
    ProfileSerializer,
    PostDetailSerializer,
    PostReadSerializer,
    FollowReadSerializer,
    LikeReadSerializer,
    CommentReadSerializer,
)
from posts.tasks import publish_scheduled_post


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user profiles.

    Provides CRUD operations for user profiles.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    @extend_schema(
        summary="Create a new profile",
        description="Creates a new user profile with the provided data",
        request=ProfileSerializer,
        responses={201: ProfileSerializer},
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "bio": "Software developer passionate about Python",
                    "profile_picture": "profile_pictures/example.jpg",
                },
                status_codes=["201"],
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing posts.

    Provides CRUD operations for posts, including scheduling posts for future publication.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        self.queryset = (
            Post.objects.prefetch_related("hashtags").select_related().filter()
        )
        return self.queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        elif self.action == "list":
            return PostReadSerializer
        return PostSerializer

    @extend_schema(
        summary="Create a new post",
        description="Creates a new post with optional scheduling for future publication",
        request=PostSerializer,
        responses={201: PostSerializer},
        examples=[
            OpenApiExample(
                "Example Request",
                value={
                    "content": "Hello, world!",
                    "image": "posts/example.jpg",
                    "scheduled_time": "2024-03-20T15:00:00Z",
                },
                status_codes=["201"],
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)
        if post.scheduled_time:
            publish_scheduled_post.apply_async(args=[post.id], eta=post.scheduled_time)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing comments on posts.

    Provides CRUD operations for comments.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    @extend_schema(
        summary="Create a new comment",
        description="Creates a new comment on a post",
        request=CommentSerializer,
        responses={201: CommentSerializer},
        examples=[
            OpenApiExample(
                "Example Request",
                value={"post": 1, "content": "Great post!"},
                status_codes=["201"],
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing likes on posts.

    Provides operations for liking and unliking posts.
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    @extend_schema(
        summary="Like a post",
        description="Adds a like to a post",
        request=LikeSerializer,
        responses={201: LikeSerializer},
        examples=[
            OpenApiExample("Example Request", value={"post": 1}, status_codes=["201"])
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user follows.

    Provides operations for following and unfollowing users.
    """

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == "list":
            return FollowReadSerializer
        return FollowSerializer

    @extend_schema(
        summary="Follow a user",
        description="Follows another user",
        request=FollowSerializer,
        responses={201: FollowSerializer},
        examples=[
            OpenApiExample(
                "Example Request", value={"following": 2}, status_codes=["201"]
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_user_id = serializer.validated_data.get("following").id
        user = request.user
        if user.id == target_user_id:
            return Response(
                {"detail": "Not allowed to follow on yourself."}, status=400
            )
        follow, created = Follow.objects.get_or_create(
            follower=user, following_id=target_user_id
        )

        if not created:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            self.get_serializer(follow).data, status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class HashtagViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing hashtags.

    Provides CRUD operations for hashtags.
    """

    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    @extend_schema(
        summary="Create a new hashtag",
        description="Creates a new hashtag",
        request=HashtagSerializer,
        responses={201: HashtagSerializer},
        examples=[
            OpenApiExample(
                "Example Request", value={"name": "python"}, status_codes=["201"]
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
