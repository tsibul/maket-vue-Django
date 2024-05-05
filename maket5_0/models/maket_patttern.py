from maket5_0.models import SettingsDictionary


class MaketPattern (SettingsDictionary):

    class Meta(SettingsDictionary.Meta):
        verbose_name = "шаблон представления в макете"
        verbose_name_plural = "шаблоны представления в макете"
        db_table_comment = 'МакетPattern'
        db_table = 'maket_pattern'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
