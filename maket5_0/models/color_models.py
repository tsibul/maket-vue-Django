from django.db import models

from maket5_0.models import SettingsDictionary, MaterialType


class ColorScheme(SettingsDictionary):
    """ color scheme IV, Grant, Eco """
    color_scheme_type = models.ForeignKey(MaterialType, on_delete=models.SET_NULL, verbose_name='материал', null=True,
                                          blank=True)

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Цветовая схема'
        verbose_name_plural = 'Цветовые схемы'
        db_table_comment = 'Color Scheme (Grant, TetraPak, Italiano Vero etc)'
        db_table = 'color_scheme'

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'color_scheme_type',
                'type': 'foreign',
                'label': 'тип материала',
                'foreignClass': 'MaterialType'
            },
        ]


class Color(SettingsDictionary):
    """ id - (07)
        name - name
        pantone - pantone color
        code - HEX"""

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        db_table_comment = 'Color'
        ordering = ['color_scheme', 'code']
        db_table = 'color'

    code = models.CharField(max_length=10, verbose_name='код')
    pantone = models.CharField(max_length=20, default='', verbose_name='PANTONE', null=True, blank=True)
    hex = models.CharField(max_length=7, verbose_name='HEX', null=True, blank=True)
    color_scheme = models.ForeignKey(ColorScheme, models.SET_NULL, null=True, verbose_name='цветовая схема')
    standard = models.BooleanField(default=True, verbose_name='стандарт')

    def __repr__(self):
        return str(self.code + ' ' + self.name + ', ' + self.color_scheme.name)

    def __str__(self):
        return str(self.code + ' ' + self.name + ', ' + self.color_scheme.name)

    @staticmethod
    def order_default():
        return ['color_scheme', 'code']

    @staticmethod
    def dictionary_fields():
        return [
            {
                'field': 'code',
                'type': 'string',
                'label': 'код',
                'null': False
            },
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'pantone',
                'type': 'string',
                'label': 'pantone',
                'null': False
            },
            {
                'field': 'hex',
                'type': 'string',
                'label': 'HEX',
                'null': False
            },
            {
                'field': 'color_scheme',
                'type': 'foreign',
                'label': 'цветовая схема',
                'foreignClass': 'ColorScheme'
            },
            {
                'field': 'standard',
                'type': 'boolean',
                'label': 'стандарт',
            },
        ]
