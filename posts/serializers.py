from rest_framework import serializers
from posts.models import Post, Comment, Hashtag, Follow, Like, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"
