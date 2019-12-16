from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountBook(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField('詳細資訊')
    create_at = models.DateTimeField('建立時間', auto_now_add=True)
    update_at = models.DateTimeField('更新時間', auto_now=True)

    def __str__(self):
        return self.title


class Authority(models.Model):
    CREATOR, READER, WRITER = range(3) 
    STATUS_CHOICES = (
        (CREATOR, 'creator'),
        (READER, 'reader'),
        (WRITER, 'writer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='使用者', related_name='share')
    book = models.ForeignKey(AccountBook, on_delete=models.CASCADE, verbose_name='帳本', related_name='book')
    authority = models.PositiveIntegerField(choices=STATUS_CHOICES, default=CREATOR)

    class Meta:
        unique_together = (
            ('user', 'book'),
        ) #合在一起為pk

    def __str__(self):
        return f'{self.user} has {self.authority} on {self.book}.'


class Category(models.Model):
    name = models.CharField(max_length=255)
    book = models.ForeignKey(AccountBook, on_delete=models.CASCADE, verbose_name='所屬帳簿', related_name='category')
    
    def __str__(self):
        return self.name


class Consume(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='付款人', related_name='paid')
    category = models.ForeignKey(Category, models.PROTECT, verbose_name='分類')
    image = models.ImageField(blank=True)
    create_at = models.DateTimeField('建立時間', auto_now_add=True)
    update_at = models.DateTimeField('更新時間', auto_now=True)

    def __str__(self):
        return self.name

class Proportion(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='付款人', related_name='percent')
    fee = models.PositiveIntegerField('費用')
    consume = models.ForeignKey(Consume, on_delete=models.CASCADE, verbose_name='消費明細', related_name='list')

    def __str__(self):
        return f'{self.username} spent {self.fee}.'