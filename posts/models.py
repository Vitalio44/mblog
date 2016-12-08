### -*- coding: utf-8 -*- ###
from __future__ import unicode_literals
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):  # For Python 2, use __unicode__ too
        return self.name

    def get_absolute_url(self):
        return reverse('show_category', kwargs={'slug': self.slug})



class Post(models.Model):
    category = models.ForeignKey(Category, default=1, verbose_name='Категория')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, verbose_name='Пользователь')
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    content = models.TextField(max_length=10000, verbose_name='Контент')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Обновлено')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Создано')
    keywords = models.CharField(max_length=1024, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'
        ordering = ["-timestamp", "-updated"]

    def __str__(self): # For Python 2, use __unicode__ too
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug, 'category': self.category})
