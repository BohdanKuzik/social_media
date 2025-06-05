from rest_framework import viewsets

from posts.models import Post, Comment, Profile, Like, Follow, Hashtag
from posts.serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
    FollowSerializer,
    HashtagSerializer,
    ProfileSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
