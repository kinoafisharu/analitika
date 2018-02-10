# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.
# Модель категории товара


class Availability(models.Model):

    def __str__(self):
        return self.availability_title

    availability_title = models.CharField(max_length=50)


class Publish(models.Model):

    def __str__(self):
        return self.publish_title

    publish_title = models.CharField(max_length=50)


class Tags(models.Model):

    def __str__(self):
        return "%s" % self.tag_title

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
        return "%s" % self.tag_title

    class Meta:
        verbose_name = 'Дополнительные теги'
        verbose_name_plural = 'Дополнительные теги'

    tag_url = models.CharField(max_length=250, unique=True)       # Ссылка на категорию
    tag_title = models.CharField(max_length=250, default=None)                  # Название категории
    tag_parent_tag = models.ForeignKey(Tags, blank=True)                  # Parents category


# Модель товара
class Offers(models.Model):

    def __str__(self):
        return "%s" % self.offer_title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    offer_title = models.CharField(max_length=250, verbose_name='Название')                       # Название товара
    offer_price = models.FloatField(default=0, verbose_name='Цена')                               # Price
    offer_valuta = models.CharField(max_length=40, verbose_name='Валюта')                       # Валюта
    offer_value = models.CharField(max_length=50, blank=True, verbose_name='Единица измерения')            # Еденица измерения товара
    offer_minorder = models.IntegerField(default=1, verbose_name='Минимальный размер заказа')
    offer_minorder_value = models.CharField(max_length=50, blank=True, verbose_name='Единица измерения минимального заказа')   # Еденица измерения товара
    offer_pre_text = models.TextField(blank=True, null=True, verbose_name='Краткое описание', default=None)                                  # Текст описания товара
    offer_text = models.TextField(verbose_name='Полное описание', default=None)                                      # Текст описания товара
    offer_availability = models.ForeignKey(Availability, verbose_name='Наличие', default=None)
    offer_publish = models.ForeignKey(Publish, verbose_name='Публикуемость', default=None)
    offer_photo = models.ImageField(blank=True, null=True, verbose_name='Фото на страницу')
    offer_url = models.CharField(max_length=250, verbose_name='Ссылка на товар на нашем сайте')                         # Ссылка на товар на нашем сайте                         # Фото на страницу ( если нету ссылки на фото)
    offer_image_url = models.URLField(null=True, blank=True, verbose_name="Ссылка на картинку", default=None)
    offer_tag = models.ForeignKey(Tags, blank=True, verbose_name='Группа 1 уровня')                      # Ссылка на категорию
    offer_subtags = models.ManyToManyField(Subtags, blank=True, verbose_name='Группа 2 уровня')          # Ссылка на категорию
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True, auto_now=False)





