from django.db import models

from maket5_0.models import SettingsDictionary


class PantoneToHex(SettingsDictionary):
    hex = models.CharField(max_length=7, null=True)

    class Meta(SettingsDictionary.Meta):
        verbose_name = "pantone_to_hex"
        verbose_name_plural = "pantone_to_hex"
        ordering = ['name']
        db_table_comment = 'PantoneToHex'
        db_table = 'pantone_to_hex'

    def __str__(self):
        return self.name + ' ' + self.hex

    def __repr__(self):
        return self.name + ' ' + self.hex

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'hex',
                'type': 'string',
                'label': 'hex',
            },
        ]