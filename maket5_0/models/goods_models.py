from django.db import models

from maket5_0.models import ColorScheme
from maket5_0.models.settings_dictionary import SettingsDictionary


class Good(SettingsDictionary):
    """details of item detail# if exist
        name - name of goods
        article - item code
        color_scheme - main color scheme"""

    article = models.CharField(max_length=30, null=True, blank=True, verbose_name='артикул')
    color_scheme = models.ForeignKey(ColorScheme, models.SET_NULL, null=True, verbose_name='цветовая схема')
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
                'field': 'detail_quantity',
                'type': 'string',
                'label': 'кол-во деталей',
                'null': False,
                'number': True
            },
        ]
