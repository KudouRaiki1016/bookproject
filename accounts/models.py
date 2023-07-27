from django.db import models
from django_mysql.models import ListCharField
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 一つのユーザーはプロフィールを一つしか持てない
    save_book_id = ListCharField(
            models.CharField(max_length=100, null=True, blank=True),max_length=(6 * 11), null=True, blank=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
# ↑sender(User)をsave()した時に↓（create_profile）が実行されるようになる（DjangoでUser登録した際は必ずその情報をsaveするように設定されているため、その際に実行させる）
def create_profile(sender, instance, created, **kwargs):
    if created:
        # -----↓Profileモデルを、userフィールドにinstance情報を積めながらcreate(新規作成)する
        Profile.objects.create(user=instance)
        # -----↑user...Profileで作成したuserフィールド
        # instance...saveしたデータ（新規作成した一人分のUser情報）が代入されてくる
    instance.profile.save()

class Class(models.Model):
    name = models.CharField("クラス名", max_length=100)
    members = models.ManyToManyField(User)
    def __str__(self):
        return str(self.name)