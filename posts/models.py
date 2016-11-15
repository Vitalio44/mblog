### -*- coding: utf-8 -*- ###
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=120, verbose_name = 'Заголовок')
    image = models.ImageField(null=True, blank=True, verbose_name = 'Изображение')
    content = models.TextField(verbose_name = 'Контент')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name = 'Обновлено')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name = 'Создано')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolut_url(self):
    	return reverse("detail", kwargs={"id": self.id})

    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'
        ordering = ["-timestamp", "-updated"]
            
    
