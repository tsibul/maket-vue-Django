from django.db import models
from maket5_0.models import CustomerType, CustomerGroup, FedRegion, SettingsDictionary


class Customer(models.Model):
    """type - agency, dealer, etc.
        number of Region"""
    form = models.CharField(max_length=255, blank=True, verbose_name='форма')
    name = models.CharField(max_length=255, verbose_name='название')
    address = models.CharField(max_length=255, blank=True, verbose_name='адрес')
    inn = models.CharField(max_length=20, null=True, verbose_name='ИНН')
    region = models.CharField(max_length=2, verbose_name='регион')
    customer_group = models.ForeignKey(CustomerGroup, models.SET_NULL, null=True, default=None,
                                       verbose_name='группа клиентов')
    customer_type = models.ForeignKey(CustomerType, models.SET_NULL, null=True, default=None,
                                      verbose_name='тип клиента')
    frigate_code = models.CharField(max_length=30, default='', db_index=True, verbose_name='фрегат id')
    phone = models.CharField(max_length=255, blank=True, verbose_name='телефон')
    mail = models.CharField(max_length=255, null=True, blank=True, verbose_name='E-mail')
    fed_region = models.ForeignKey(FedRegion, models.SET_NULL, null=True, default=None,
                                   verbose_name='федеральный округ')
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        db_table_comment = 'Customer'
        db_table = 'customer'
        ordering = ['name']

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def order_default():
        return ['name']

    @staticmethod
    def dictionary_fields():
        return [
            {
                'field': 'form',
                'type': 'string',
                'label': 'форма',
                'readonly': 'true'
            },
            {
                'field': 'name',
                'type': 'string',
                'label': 'название',
                'readonly': 'true'
            },
            {
                'field': 'address',
                'type': 'string',
                'label': 'адрес',
                'readonly': 'true'
            },
            {
                'field': 'inn',
                'type': 'string',
                'label': 'ИНН',
                'readonly': 'true'
            },
            {
                'field': 'region',
                'type': 'string',
                'label': 'регион',
                'null': False,
                'readonly': 'true'
            },
            {
                'field': 'customer_group',
                'type': 'foreign',
                'label': 'группа',
                'foreignClass': 'CustomerGroup',
                'readonly': 'true'
            },
            {
                'field': 'customer_type',
                'type': 'foreign',
                'label': 'тип',
                'foreignClass': 'CustomerType'
            },
            {
                'field': 'frigate_code',
                'type': 'string',
                'label': 'fr id',
                'readonly': 'true'
            },
            {
                'field': 'phone',
                'type': 'string',
                'label': 'телефон',
                'readonly': 'true'
            },
            {
                'field': 'mail',
                'type': 'string',
                'label': 'E-mail',
                'readonly': 'true'
            },
            {
                'field': 'fed_region',
                'type': 'foreign',
                'label': 'округ',
                'foreignClass': 'FedRegion',
            },
        ]


class Manager(SettingsDictionary):
    """Customer managers """
    phone = models.CharField(max_length=50, blank=True, null=True, default='')
    mail = models.CharField(max_length=50, blank=True, null=True, default='')
    customer_group = models.ForeignKey(CustomerGroup, models.SET_NULL, null=True, default=None,)

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Менеджер клиента'
        verbose_name_plural = 'Менеджеры клиентов'
        db_table_comment = 'Manager'
        db_table = 'manager'

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'phone',
                'type': 'string',
                'label': 'телефон',
            },
            {
                'field': 'mail',
                'type': 'string',
                'label': 'почта',
            },
            {
                'field': 'customer_group',
                'type': 'foreign',
                'label': 'группа',
                'foreignClass': 'CustomerGroup',
                'readonly': 'true'
            },
        ]
