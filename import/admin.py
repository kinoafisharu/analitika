# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Делаем импорт настроек для импорта-экспорта.
from .resource import *
from import_export.formats.base_formats import *
# Делаем наследование от ImportExportModelAdmin, вместо обычного admin.AdminModels.
# Для подключение батарейке к моделе необходимо указывать наследование от ImportExportModelAdmin
# Он отвечает за импорт-экспорт в моделе.


class OfferAdmin(ImportExportModelAdmin):
    search_fields = ('offer_title', )
    list_display = ('offer_title',)
    prepopulated_fields = {'slug': ('offer_title',)}
    #Подключаем нужные настройки для импорта и экспорта.
    resource_class = OfferResource

    # Указываем форматы экспорта.
    def get_export_formats(self):
        return [CSV, XLS, XLSX, TSV, JSON, HTML]

    # Указываем форматы импорта.
    def get_import_formats(self):
        return [CSV, XLS, XLSX, TSV, JSON, HTML]

admin.site.register(Offers, OfferAdmin)
admin.site.register(Subtags)
admin.site.register(Tags)
