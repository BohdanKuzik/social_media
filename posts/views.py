from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

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


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == "list":
            return FollowReadSerializer
        return FollowSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_user_id = serializer.validated_data.get("following").id
        user = request.user
        if user.id == target_user_id:
            return Response({"detail": "Not allowed to follow on yourself."}, status=400)
        follow, created = Follow.objects.get_or_create(
            follower=user,
            following_id=target_user_id
        )

        if not created:
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(self.get_serializer(follow).data, status=status.HTTP_201_CREATED)


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Post.objects.all()

    def get_queryset(self):
        self.queryset = Post.objects.prefetch_related("hashtags").select_related().filter(published=True)
        return self.queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        elif self.action == "list":
            return PostReadSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == "list":
            return LikeReadSerializer
        return LikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        target_post_id = serializer.validated_data.get("post").id
        user = request.user
        like, created = Like.objects.get_or_create(
            user=user,
            post_id=target_post_id
        )
        if not created:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(self.get_serializer(like).data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == "list":
            return CommentReadSerializer
        return CommentSerializer


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
