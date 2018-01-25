from .models import *
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export import fields
from import_export import resources

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
