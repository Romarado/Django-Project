from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .middleware import get_current_user
from django.db.models import Q


class Bugurt(models.Model):
    bugurtName = models.CharField('Название бугурта', max_length=20)
    bugurtTheme = models.CharField('Тема бугурта', max_length=20)
    bugurtAsIs = models.TextField('Бугурт')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор записи", blank=True, null=True)

    def __str__(self):
        return self.bugurtName + " " + self.bugurtTheme + " " + self.bugurtAsIs

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})

    # def get_absolute_url(self):
    #     return reverse("bugurt")


class Racer(models.Model):
    name = models.CharField('Название бугурта', max_length=20)
    surname = models.CharField('Тема бугурта', max_length=20)
    abilities = models.TextField('Бугурт')
    datetime = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор записи", blank=True, null=True)

    def __str__(self):
        return self.name + " " + self.surname + " " + self.abilities

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})


class StatusFilterComments(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status=False, author=get_current_user() ) |
                                             Q(status=False, article__author=get_current_user()) |
                                             Q(status=True))


class Comments(models.Model):
    article = models.ForeignKey(Bugurt, on_delete=models.CASCADE, verbose_name='Бугурт', blank=True, null=True,
                                related_name='comments_bugurts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор записи", blank=True, null=True)
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)
    objects = StatusFilterComments()

    def __str__(self):
        return str(self.article) + ' ' + str(self.author) + ' ' + str(self.text) + ' ' + str(self.status)


