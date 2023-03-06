from django.db import models
from .consts import MAX_RATE
from django.contrib.auth.models import User
from django.utils import timezone
from django_mysql.models import ListTextField

RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_RATE + 1)]

CATEGORY = (('business', 'ビジネス'), ('life','生活'), ('other','その他'))
class Book(models.Model):
    title = models.CharField(max_length = 100)
    text = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    category = models.CharField(
        max_length = 100,
        choices = CATEGORY
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '本のデータ'

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# ----------投稿に対するいいね----------
class LikeForBook(models.Model):
    """投稿に対するいいね"""
    target = models.ForeignKey(Book, on_delete=models.CASCADE) # いいね対象書籍
    user = models.ForeignKey(User, on_delete=models.CASCADE) # いいねしたUser
    timestamp = models.DateTimeField(default=timezone.now) # いいねしたタイミング
# ----------

release_choice = ((True, '公開'),(False, '非公開'))
class Folder(models.Model):
    title = models.CharField(max_length=100)
    release = models.BooleanField(choices=release_choice)
    # ----------編成情報を詰め込んでいくリスト----------
    post_list = ListTextField(
        base_field=models.IntegerField(), # これで数値型で管理できるようになる？
        size=100,  # Maximum of 100 ids in list(要素数は100個まで？)
        )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)