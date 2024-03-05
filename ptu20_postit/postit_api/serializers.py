from rest_framework import serializers
from . import models


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    user_username = serializers.ReadOnlyField(source='user.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = models.Comment
        fields = [
            'id', 'body', 'post',
            'created_at', 'updated_at',
            'user_id', 'user_username',
        ]


class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    user_username = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return models.Comment.objects.filter(post=obj).count()
    
    def get_like_count(self, obj):
        return models.PostLike.objects.filter(post=obj).count()

    class Meta:
        model = models.Post
        fields = [
            'id', 'title', 'body', 'image',
            'created_at', 'updated_at',
            'user_id', 'user_username',
            'like_count', 'comment_count', 'comments',
        ]


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = models.PostLike
        fields = ['id', 'user', 'post']


class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    comment = serializers.ReadOnlyField(source='comment.id')

    class Meta:
        model = models.CommentLike
        fields = ['id', 'user', 'comment']
