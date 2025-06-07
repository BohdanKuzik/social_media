from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import Post, Comment, Hashtag, Follow, Like, Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "profile_picture",
        ]


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = [
            "following",
            "followed_at",
        ]


class FollowReadSerializer(FollowSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = [
            "follower",
            "following",
            "followed_at",
        ]


class LikeSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = [
            "post",
            "created_at",
        ]

class LikeReadSerializer(LikeSerializer):
    post = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = [
            "post",
            "created_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = [
            "post",
            "text",
            "created_at",
        ]


class CommentReadSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "post",
            "text",
            "created_at",
        ]


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = [
            "name",
        ]


class PostSerializer(serializers.ModelSerializer):
    hashtags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Hashtag.objects.all()
    )
    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "image",
            "hashtags",
            "published",
            "scheduled_time",
        ]

class PostReadSerializer(serializers.ModelSerializer):
    hashtags = HashtagSerializer(many=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "content",
            "image",
            "hashtags",
            "published",
            "like_count",
        ]


class PostDetailSerializer(PostSerializer):
    likes = serializers.StringRelatedField(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ["likes", "scheduled_time"]
