from django.db import models

from maket5_0.models import ColorScheme
from maket5_0.models.settings_dictionary import SettingsDictionary


class Good(SettingsDictionary):
    """details of item detail# if exist
        name - name of goods
        article - item code
        color_scheme - main color scheme"""

    article = models.CharField(max_length=30, null=True, blank=True)
    color_scheme = models.ForeignKey(ColorScheme, models.SET_NULL, null=True)
    detail_quantity = models.SmallIntegerField(default=1)

    class Meta(SettingsDictionary.Meta):
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ['article']
        db_table_comment = 'Goods'
        db_table = 'goods'

    def __repr__(self):
        return self.article

    def __str__(self):
        return str(self.article)

    @staticmethod
    def order_default():
        return ['article']
