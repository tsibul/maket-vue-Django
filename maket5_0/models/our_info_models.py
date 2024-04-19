from django.db import models
from maket5_0.models import SettingsDictionary


class OurCompany(SettingsDictionary):
    """ """
    code = models.CharField(max_length=4, default='ВВ', null=False, blank=False)

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'
        db_table_comment = 'Our Companies'
        db_table = 'our_companies'

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code

    @staticmethod
    def dictionary_fields():
        return [
            {
                'field': 'code',
                'type': 'string',
                'label': 'код',
                'null': False
            },
            SettingsDictionary.dictionary_fields()[0]
        ]
