from django.db import models

from maket5_0.models.settings_dictionary import SettingsDictionary


class FedRegion(SettingsDictionary):
    """Fed Region Model"""

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Федеральный округ'
        verbose_name_plural = 'Федеральные округа'
        db_table_comment = 'Federal Region Model'
        db_table = 'fed_region'


class RegionToFedRegion(SettingsDictionary):
    """Region to Federal Region correspondence"""
    fed_region = models.ForeignKey(FedRegion, on_delete=models.CASCADE, verbose_name='федеральный округ')

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Соответствие ИНН и федерального округа'
        verbose_name_plural = 'Соответствие ИНН и федерального округов'
        db_table_comment = 'Region to Federal Region correspondence'
        db_table = 'region_to_fed_region'

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'fed_region',
                'type': 'foreign',
                'label': 'федеральный округ',
                'foreignClass': 'FedRegion'
            },
        ]


class TypeGroup(SettingsDictionary):
    """ group type agency, dealer etc."""

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Тип группы'
        verbose_name_plural = 'Типы групп'
        db_table_comment = 'Group Type'
        db_table = 'type_group'


class CustomerType(SettingsDictionary):
    """Customer Type dealer, agency etc."""
    group_discount = models.FloatField(default=0, verbose_name='скидка')
    code = models.CharField(max_length=2, default='', verbose_name='код группы')
    type_group = models.ForeignKey(TypeGroup, models.SET_NULL, null=True, blank=True, default=None,
                                   verbose_name='тип группы')

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Тип клиента'
        verbose_name_plural = 'Типы клиентов'
        db_table_comment = 'Customer Type'
        db_table = 'customer_type'

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'group_discount',
                'type': 'string',
                'label': 'скидка',
                'null': False,
                'number': True
            },
            {
                'field': 'code',
                'type': 'string',
                'label': 'код группы',
                'null': False
            },
            {
                'field': 'type_group',
                'type': 'foreign',
                'label': 'тип группы',
                'foreignClass': 'TypeGroup'
            },
        ]


class CustomerGroup(SettingsDictionary):
    """Customer Group
    customer_type — type of client (agency, dealer, etc.)
    default — if group consist from one customer"""
    customer_type = models.ForeignKey(CustomerType, models.SET_NULL, null=True, verbose_name='тип клиента')
    phone = models.CharField(max_length=255, default='', verbose_name='телефон', blank=True, null=True)
    mail = models.CharField(max_length=255, default='', verbose_name='E-mail', null=True, blank=True)
    default = models.BooleanField(default=True, verbose_name='стандарт')
    fed_region = models.ForeignKey(FedRegion, models.SET_NULL, null=True, blank=True, default=None,
                                   verbose_name='федеральный округ')

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Группа клиентов'
        verbose_name_plural = 'Группы клиентов'
        db_table_comment = 'Customer Group'
        db_table = 'customer_group'

    def default_group(self, customer):
        self.name = customer.name
        self.phone = customer.phone
        self.mail = customer.mail
        self.default = True
        self.customer_type = customer.customer_type
        region_to_region = RegionToFedRegion.objects.filter(name=customer.inn[0:2]).first()
        if region_to_region:
            self.fed_region = region_to_region.fed_region

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'customer_type',
                'type': 'foreign',
                'label': 'тип клиента',
                'foreignClass': 'CustomerType'
            },
            {
                'field': 'phone',
                'type': 'string',
                'label': 'телефон',
            },
            {
                'field': 'mail',
                'type': 'string',
                'label': 'E-mail',
            },
            {
                'field': 'default',
                'type': 'boolean',
                'label': 'стандарт',
                'null': False
            },
            {
                'field': 'fed_region',
                'type': 'foreign',
                'label': 'федеральный округ',
                'foreignClass': 'FedRegion'
            },
        ]


class CustomerGroupFrigateId(models.Model):
    customer_group = models.ForeignKey(CustomerGroup, on_delete=models.CASCADE, verbose_name='группа клиентов')
    frigate_code = models.CharField(max_length=30, unique=True, verbose_name='фрегат id')

    class Meta:
        verbose_name = 'Группа клиентов'
        verbose_name_plural = 'Группы клиентов'
        db_table_comment = 'Customer Group Frigate ID'
        db_table = 'customer_group_frigate_id'
