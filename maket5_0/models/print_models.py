from maket5_0.models import SettingsDictionary


class PrintType(SettingsDictionary):
    """ Pad, screen, UW, soft_touch etc."""

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'тип печати'
        verbose_name_plural = 'типы печати'
        db_table_comment = 'Print Type'
        db_table = 'print_type'


class PrintPlace(SettingsDictionary):
    """ Print Place from Import"""

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'место нанесения'
        verbose_name_plural = 'места нанесения'
        db_table_comment = 'Print Place'
        db_table = 'print_place'


class PrintPosition(SettingsDictionary):
    """ Print Position from Maket"""

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'положение нанесения'
        verbose_name_plural = 'положения печати'
        db_table_comment = 'Print Position'
        db_table = 'print_position'
