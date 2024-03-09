from maket5_0.models import SettingsDictionary


class MaterialType(SettingsDictionary):
    """ plastic, metal, paper, block printing etc"""

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Материал'
        verbose_name_plural = 'Типы материала'
        db_table_comment = 'Material Type (plastic, metal, paper, block printing etc)'
        db_table = 'material_type'

