from django.db import models
from django.core.files.storage import FileSystemStorage

from maket5_0.models import SettingsDictionary, Good

fs_additional = FileSystemStorage(location='maket5_0/files/patterns')


class Pattern(SettingsDictionary):
    file = models.FileField(storage=fs_additional, null=True, blank=True)
    good = models.ForeignKey(Good, models.SET_NULL, null=True, blank=True)

    class Meta(SettingsDictionary.Meta):
        verbose_name = "шаблон нанесения"
        verbose_name_plural = "шаблоны нанесения"
        ordering = ['good__article']
        db_table_comment = 'Pattern'
        db_table = 'patern'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def order_default():
        return ['good__article']

    @staticmethod
    def dictionary_fields():
        return [

            {
                'field': 'good',
                'type': 'foreign',
                'label': 'продукция',
                'foreignClass': 'Good',
                'null': False
            },
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'file',
                'type': 'file',
                'label': 'шаблон нанесения',
                'number': False,
                'null': True,
                'emitChoices': False
            },
        ]
