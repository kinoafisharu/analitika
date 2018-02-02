# -*- coding: utf-8 -*-
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Делаем импорт настроек для импорта-экспорта.
from .resource import *
from import_export.formats.base_formats import *
# Делаем наследование от ImportExportModelAdmin, вместо обычного admin.AdminModels.
# Для подключение батарейке к моделе необходимо указывать наследование от ImportExportModelAdmin
# Он отвечает за импорт-экспорт в моделе.
import ast
import json

from import_export.formats.base_formats import JSON as _JSON
#Настройка типа файла json, для отображения кирилицы.
# --------dataset-------
# offer_title         |slug              |offer_price|dimension|offer_tag       |offer_sub_tag
# --------------------|------------------|-----------|---------|----------------|------------------------------------------------------------------------------------------------
# ВВГнг А 4 35 ок 0 66|vvgng-4-35-ok-0-66|2222.0     |м        |. Кабель, провод|vvgng_a_kabel_silovoy_mednyy_s_pvkh_izolyatsiey_ne_rasprostranyayushchiy_gorenie, 1_kabel_provod
# -------dataset.dict----------
# [OrderedDict([('offer_title', 'ВВГнг А 4 35 ок 0 66'), ('slug', 'vvgng-4-35-ok-0-66'), ('offer_price', '2222.0'),
# ('dimension', 'м'), ('offer_tag', '. Кабель, провод'), ('offer_sub_t
# ag', 'vvgng_a_kabel_silovoy_mednyy_s_pvkh_izolyatsiey_ne_rasprostranyayushchiy_gorenie, 1_kabel_provod')])]
# -----------------------------
#  for k, v in row.items() перебираем ключ значения и формируем json.
# -------ast.literal_eval( node_or_string )----------
# Обрабатываем наш словарь для формирование корректного json-a
# Безопасная оценка узла выражения или строки, содержащей литеральный или контейнерный дисплей Python.
# Представленная строка или узел могут состоять только из следующих литеральных структур Python:
# строки, байты, числа, кортежи, списки, dicts, sets, booleans и т None.
# -----------------------------
# ensure_ascii=False. Возращает строку вместо unicode. Следовательно корректно записуем кирилицу
class JSON(_JSON):
    def export_data(self, dataset, **kwargs):
        data = []
        for row in dataset.dict:
            row_fix = {}
            data.append(row_fix)
            for k, v in row.items():
                if isinstance(v, str) and (v.startswith("{'") and v.endswith("'}")):
                    v = ast.literal_eval(v)
                if isinstance(v, str) and (v.startswith("['") and v.endswith("']")):
                    v = ast.literal_eval(v)
                row_fix[k] = v
        return json.dumps(data, ensure_ascii=False)

    def get_content_type(self):
        return 'application/json; charset=utf-8'

class OfferAdmin(ImportExportModelAdmin):
    search_fields = ('offer_title', )
    list_display = ('offer_title',)
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
admin.site.register(Availability)
admin.site.register(Publish)
admin.site.register(Tags)
