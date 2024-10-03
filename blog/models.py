from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.utils import timezone, dateformat
from django.template.defaultfilters import timesince
from datetime import timedelta


class Post(models.Model):
    """
    Модель Post (Пост).

    Эта модель представляет пост в блоге. Сортировка по убыванию по дате создания поста.

    Using in:
        - Views: `FeedView`, `PostsView`, `PostDetailView`, `AddPostView`, `UpdatePostView`, `DeletePostView`.
        - Forms: `AddPostForm`.
        - Templates: `blog/add_post.html`, `blog/delete_post.html`, `blog/feed_page.html`,
         `blog/post_detail.html`, `blog/posts.html`, `blog/update_post.html`, `blog/user_posts.html`.

    Fields:
        - title (str): Заголовок поста.
        - content (str): Текст поста.
        - author (User): Автор поста.
        - slug (str): Строка используемая для построения адреса к посту.
        - last_modified (datetime.datetime): Дата последнего изменения поста.
        - date_created (datetime.datetime): Дата создания поста.
    """
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
#    status = models.CharField(max_length=10, default="draft", help_text="May be either 'draft' or 'published")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(db_index=True, unique=True)
    last_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
#    pub_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created'], name='IDX_posts_datecreated'),
        ]

    def __str__(self):
        """
        Возвращает строковое представление поста.

        Returns:
            str: Заголовок поста.
        """
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={'slug': self.slug})

    def timesince(self):
        """
        Дата создания поста или время прошедшее с даты публикации.

        Время возвращается в трёх вариантах:
            - '1 января 2000' - если период более года.
            - '1 января 2000 12:00' - если период менее года но более недели.
            - '1 день|час|минуту назад' - если период менее недели.

        Using in:
            - Templates: `blog/feed_page.html`, `blog/user_posts.html`, `blog/posts.html`, `blog/post_detail.html`.

        Returns:
            str: Дата создания или период с даты создания.
        """
        diff = timezone.now() - self.date_created
        if diff < timedelta(days=365):
            if diff > timedelta(days=7):
                format = 'd M в H:i'
            else:
                return timesince(self.date_created, timezone.now()).split(',')[0] + ' назад'
        else:
            format = 'd E Y'
        return dateformat.format(self.date_created, format)

#    def clean(self):
#        if self.status == 'draft' and self.pub_date is not None:
#            raise ValidationError(
#                {"pub_date": _("Черновики не могут иметь дату публикации")}
#            )
#        if self.status == "published" and self.pub_date is None:
#            self.pub_date = timezone.now()


class Comment(models.Model):
    """
    Модель Comment (Комментарий)

    Представляет комментарий к посту (`Post`). Сортировка по убыванию по дате создания комментария.

    Using in:
        - Views: `PostDetailView`.
        - Forms: `AddCommentForm`.
        - Templates: `blog/post_detail.html`, `blog/comments_tree.html`, `blog/comment_snippet.html`.
    Fields:
        - post (Post): Пост, к которому прикрепляется комментарий.
        - author (User): Автор комментария.
        - text (str): Текст комментария.
        - date_created (datetime.datetime): Дата создания комментария.
        - parent_comment (Comment): Указывает на комментарий, к которому сделан комментарий.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=900)
    date_created = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self',
                                       on_delete=models.CASCADE,
                                       null=True, blank=True,
                                       related_name='child_comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date_created']
        indexes = [
            models.Index(fields=['-date_created'], name='IDX_comments_datecreated'),
        ]

    def __str__(self):
        if self.parent_comment:
            return f"{self.author}'s comment on {self.parent_comment.author}s comment with pk={self.parent_comment.pk}"
        return f"{self.author}'s comment on '{self.post}'"

    # def has_parent(self):
    #     return self.parent_comment is not None

    @staticmethod
    def make_recursive_comments_list(comments, level=0):
        """
        Возвращает рекурсивное дерево комментариев

        Возвращает список словарей, где каждый словарь содержит сам комментарий, отступ, и его дочерние комментарии.
        Позволяет в шаблонах построить дерево сообщений.

        Args:
            comments (QuerySet): QuerySet с комментариями
            level (int): отступ

        Returns:
            list: Список словарей с полями 'comment', 'indent' и 'child_comments'
        """
        def recursive_builder(comment, level):
            result = {
                'comment': comment,
                'indent': level * 1,
                'child_comments': []
            }
            for child in comment.child_comments.all():
                result['child_comments'].append(recursive_builder(child, level + 1))
            return result

        tree = []
        for comment in comments.filter(parent_comment=None):
            tree.append(recursive_builder(comment, level))
        return tree
