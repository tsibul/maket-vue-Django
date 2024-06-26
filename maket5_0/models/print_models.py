from django.db import models
from maket5_0.models import SettingsDictionary


class PrintType(SettingsDictionary):
    """ Pad, screen, UW, soft_touch etc.
    printable: if show in maket
    """
    printable = models.BooleanField(default=True)

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'printable',
                'type': 'boolean',
                'label': 'печатается',
            },
        ]

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'тип печати'
        verbose_name_plural = 'типы печати'
        db_table_comment = 'Print Type'
        db_table = 'print_type'


class PrintPlace(SettingsDictionary):
    """ Print Place from Import"""

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'место нанесения (деталь)'
        verbose_name_plural = 'места нанесения (детали)'
        db_table_comment = 'Print Place'
        db_table = 'print_place'


class PrintPosition(SettingsDictionary):
    """ Print Position from Maket"""

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'ориентация нанесения'
        verbose_name_plural = 'ориентации печати'
        db_table_comment = 'Print Position'
        db_table = 'print_position'


class PrintPlaceToPrintPosition(SettingsDictionary):
    """PrintPlace to PrintPosition Correspondence"""
    print_place = models.ForeignKey(PrintPlace, on_delete=models.CASCADE)
    print_position = models.ForeignKey(PrintPosition, on_delete=models.CASCADE)

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'соответствие места и ориентации нанесения'
        verbose_name_plural = 'соответствие места и ориентации нанесения'
        ordering = ['print_place__name']
        db_table_comment = 'Print Place to Print Position'
        db_table = 'print_place_to_print_position'

    def __repr__(self):
        return self.print_place.name + ' ' + self.print_position.name

    def __str__(self):
        return self.print_place.name + ' ' + self.print_position.name

    @staticmethod
    def order_default():
        return ['print_place__name']

    @staticmethod
    def dictionary_fields():
        return [
            {
                'field': 'print_place',
                'type': 'foreign',
                'label': 'место нанесения',
                'foreignClass': 'PrintPlace',
                'null': False
            },
            {
                'field': 'print_position',
                'type': 'foreign',
                'label': 'позиция нанесения',
                'foreignClass': 'PrintPosition',
                'null': False
            },
        ]

