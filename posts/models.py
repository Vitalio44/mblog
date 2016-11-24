### -*- coding: utf-8 -*- ###
from __future__ import unicode_literals
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.conf import settings
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, verbose_name='Пользователь')
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    content = models.TextField(max_length = 10000, verbose_name='Контент')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Обновлено')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'
        ordering = ["-timestamp", "-updated"]

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})

