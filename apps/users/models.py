from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    '''
    用户
    '''
    # blank
    # 是针对表单的，如果
    # blank = True，表示你的表单填写该字段的时候可以不填,
    # null等于true表示数据库中该字段为True.
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name='电话')
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', '女')), default='female',
                              verbose_name='性别')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    # 获取django中的model字段名
    # 字段的verbose_name

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    '''
    短信验证码
    '''
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    # models.Model的内部类Meta,存在两个特殊的选项,verbose_name,verbose_name_plural,
    # verbose_name为model提供了一个更容易让人阅读的名称,而verbose_name_plural则是
    # 这个名称的复数形式.
    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
