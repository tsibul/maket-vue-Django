from django.db import models

from maket5_0.models import SettingsDictionary


class MaketPattern(SettingsDictionary):
    """
    Pattern for maket layout
    comment: comment
    """
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta(SettingsDictionary.Meta):
        verbose_name = "шаблон представления в макете"
        verbose_name_plural = "шаблоны представления в макете"
        db_table_comment = 'МакетPattern'
        db_table = 'maket_pattern'

    def __str__(self):
        add_str = ''
        if self.comment:
            add_str = ' ' + self.comment
        return self.name + add_str

    def __repr__(self):
        add_str = ''
        if self.comment:
            add_str = ' ' + self.comment
        return self.name + add_str

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'comment',
                'type': 'string',
                'label': 'описание',
            },
        ]
