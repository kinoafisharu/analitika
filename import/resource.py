from .models import *
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export import fields
from import_export import resources
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


# По умолчанию ModelResource, исследует поля модели и создает Field-трибуты с соответствующим Widget для каждого поля.
# Чтобы повлиять на то, какие поля модели будут включены в ресурс импорта-экспорта переопределим эти настройки.
# Потому что по умолчание стоит pk(id поля). Мы же делаем по названию или как захотим.
class OfferResource(resources.ModelResource):
    offer_title = fields.Field(
        column_name='offer_title',
        attribute='offer_title')
    slug = fields.Field(
        column_name='slug',
        attribute='slug')
    offer_price = fields.Field(
        column_name='offer_price',
        attribute='offer_price')
    dimension = fields.Field(
        column_name='dimension',
        attribute='dimension')
    # Настройка полей для экспорта и импорта. Поле связаное по ключу.
    offer_tag = fields.Field(
        column_name='offer_tag',
        attribute='offer_tag',
        widget=ForeignKeyWidget(Tags, 'tag_title'))
    # Настройка полей для экспорта и импорта. Поле связаное по многое-ко-многому. Ниже продолжение настроек.
    offer_sub_tag = fields.Field(widget=ManyToManyWidget(Subtags, 'tag_title'))

    class Meta:
        model = Offers
        import_id_fields = ['slug']
        fields = ('offer_title', 'slug', 'offer_price', 'dimension', 'offer_tag', 'offer_sub_tag')

    # Настройка полей для экспорта и импорта. Поле связаное по многое-ко-многому. Выводим все значение. Функция описана в док. к батарейке
    def dehydrate_offer_sub_tag(self, offers):
        colls = [coll.tag_title for coll in offers.offer_sub_tag.all()]
        collectors = ', '.join(colls)

        return '%s' % collectors
