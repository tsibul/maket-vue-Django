from django.db import models

from maket5_0.models import ColorScheme, MaketPattern
from maket5_0.models.settings_dictionary import SettingsDictionary


class GoodsImagesSet(SettingsDictionary):
    """Set of Images of each detail
    images_quantity — size of images set"""
    images_quantity = models.IntegerField(verbose_name='количество изображений элемента')

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Набор изображений изделия'
        verbose_name_plural = 'Наборы изображений изделий'
        db_table_comment = 'Set of Goods Images'
        db_table = 'goods_images_set'

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'images_quantity',
                'type': 'string',
                'label': 'кол-во видов',
                'number': True,
                'null': False,
                'emitChoices': True
            },
        ]


class Good(SettingsDictionary):
    """details of item detail# if exist
        name - name of goods
        article - item code
        color_scheme - main color scheme
        maket_pattern - layout in maket_layout
        """

    article = models.CharField(max_length=30, null=True, blank=True, verbose_name='артикул')
    color_scheme = models.ForeignKey(ColorScheme, models.SET_NULL, null=True, verbose_name='цветовая схема')
    maket_pattern = models.ForeignKey(MaketPattern, models.SET_NULL, null=True, verbose_name='размещение в макете')
    goods_images_set = models.ForeignKey(GoodsImagesSet, models.SET_NULL, null=True, verbose_name='набор шаблонов')
    detail_quantity = models.SmallIntegerField(default=1, verbose_name='количество деталей')

    class Meta(SettingsDictionary.Meta):
        verbose_name = "продукция"
        verbose_name_plural = "продукция"
        ordering = ['article']
        db_table_comment = 'Goods'
        db_table = 'goods'

    def __repr__(self):
        return self.article + ' ' + self.name

    def __str__(self):
        return str(self.article) + ' ' + str(self.name)

    @staticmethod
    def order_default():
        return ['article']

    @staticmethod
    def dictionary_fields():
        return [
            {
                'field': 'article',
                'type': 'string',
                'label': 'артикул',
                'null': False
            },
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'color_scheme',
                'type': 'foreign',
                'label': 'цветовая схема',
                'foreignClass': 'ColorScheme',
                'null': False
            },
            {
                'field': 'maket_pattern',
                'type': 'foreign',
                'label': 'вид блока в макете',
                'foreignClass': 'MaketPattern',
            },
            {
                'field': 'goods_images_set',
                'type': 'foreign',
                'label': 'набор шаблонов',
                'foreignClass': 'GoodsImagesSet',
            },
            {
                'field': 'detail_quantity',
                'type': 'string',
                'label': 'кол-во деталей',
                'null': False,
                'number': True,
                'emitChoices': True
            },
        ]
