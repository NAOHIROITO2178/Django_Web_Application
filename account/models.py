from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    bio = models.TextField(max_length=1000, blank=True, null=True, verbose_name='自己紹介')
    job_title = models.CharField(max_length=50, choices=[
        ('Non_selected', ''),
        ('Engineer', 'エンジニア'),
        ('Designer', 'デザイナー'),
        ('Marketer', 'マーケター'),
        ('Director', 'ディレクター'),
        ('Sales', '営業'),
        ('CxO', 'CxO'),
        ('Other', 'その他')
    ], blank=True, null=True, verbose_name='職種')
    
    # related_nameを追加して衝突を回避
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )
