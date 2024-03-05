from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse


class UserModel(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        _("created at"), 
        auto_now_add=True, 
        db_index=True
    )
    updated_at = models.DateTimeField(
        _("updated at"), 
        auto_now=True, 
        db_index=True
    )

    def get_absolute_url(self):
        try:
            url = reverse(
                f"{self.__class__.__name__.lower()}_detail", 
                kwargs={"pk": self.pk}
            )
        except Exception as e:
            print(e)
        else:
            return url 

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Post(UserModel):
    title = models.CharField(_("title"), max_length=150)
    body = models.TextField(_("body"), max_length=10000)
    image = models.ImageField(_("image"), upload_to='post_images', null=True)

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.title


class Comment(UserModel):
    body = models.TextField(_("body"), max_length=10000)
    post = models.ForeignKey(
        Post, 
        verbose_name=_("post"), 
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self) -> str:
        return "{} {} {}".format(
            self.post,
            _("commented by"),
            self.user,
        )

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")


class PostLike(UserModel):
    post = models.ForeignKey(
        Post, 
        verbose_name=_("post"), 
        on_delete=models.CASCADE,
        related_name='likes',
    )

    class Meta:
        verbose_name = _("post like")
        verbose_name_plural = _("post likes")

    def __str__(self):
        return "{} {} {}".format(
            self.post,
            _("liked by"),
            self.user,
        )


class CommentLike(UserModel):
    comment = models.ForeignKey(
        Comment, 
        verbose_name=_("comment"), 
        on_delete=models.CASCADE,
        related_name='likes',
    )

    class Meta:
        verbose_name = _("comment like")
        verbose_name_plural = _("comment likes")

    def __str__(self):
        return "{} {} {}".format(
            self.comment,
            _("liked by"),
            self.user,
        )
