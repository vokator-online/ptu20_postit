from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models, serializers


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
