# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.
# Модель категории товара
class Tags(models.Model):

    def __str__(self):
        return self.tag_title

    class Meta:
        verbose_name = 'Основные теги'
        verbose_name_plural = 'Основные теги'

    tag_url = models.CharField(max_length=250, unique=True)     # Ссылка на категорию
    tag_title = models.CharField(max_length=250)               # Название категории
    tag_publish = models.BooleanField(blank=True)
    tag_priority = models.IntegerField(blank=True)



# Модель категории товара
class Subtags(models.Model):

    def __str__(self):
        return self.tag_title

    class Meta:
        verbose_name = 'Дополнительные теги'
        verbose_name_plural = 'Дополнительные теги'

    tag_url = models.CharField(max_length=250, unique=True)       # Ссылка на категорию
    tag_title = models.CharField(max_length=250)                  # Название категории
    tag_parent_tag = models.ForeignKey(Tags, blank=True)                  # Parents category

    @classmethod
    def create(cls, tag_title):
        tag = cls(tag_title=tag_title, tag_url=slugify_url(tag_title))
        tag.save()
        # do something with the book
        return tag


# Модель товара
class Offers(models.Model):

    def __str__(self):
        return self.offer_title

    class Meta:
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    offer_title = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True)# Название товара
    offer_price = models.FloatField(default=0, verbose_name='Цена')                           # Price                     # Валюта
    dimension = models.CharField(max_length=50, blank=True, verbose_name='Единица измерения')            # Еденица измерения товара
    offer_tag = models.ForeignKey(Tags, blank=True, verbose_name='Группа 1 уровня')                      # Ссылка на категорию
    offer_sub_tag = models.ManyToManyField(Subtags, blank=True, verbose_name='Группа 2 уровня')          # Ссылка на категорию





