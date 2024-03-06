from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from . import models, serializers


class UserCreate(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]


class UserDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        if request.user:
            request.user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_("User does not exist."))


class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = models.Post.objects.filter(
            pk=kwargs['pk'], user=self.request.user
        )
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can only delete your own content."))
    
    def put(self, request, *args, **kwargs):
        post = models.Post.objects.filter(
            pk=kwargs['pk'], user=self.request.user
        )
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can only edit your own content."))


class CommentList(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)

    def get_queryset(self):
        queryset = models.Comment.objects.all()
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return queryset.filter(post=post)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(
            pk=kwargs['pk'], user=self.request.user
        )
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can only delete your own content."))
    
    def put(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(
            pk=kwargs['pk'], user=self.request.user
        )
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can only edit your own content."))


class PostLikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]
        
    def get_queryset(self):
        queryset = models.PostLike.objects.all()
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return queryset.filter(post=post, user=self.request.user)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_("You already like this."))
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(post=post, user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_("You must already like this to unlike this."))
