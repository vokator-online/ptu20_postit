from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Post
        fields = [
            'id', 'title', 'body', 
            'created_at', 'updated_at',
            'user_id', 'user_username',
        ]
