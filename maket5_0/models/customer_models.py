from django.db import models
from maket5_0.models import CustomerType, CustomerGroup, FedRegion


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
    frigate_code = models.CharField(max_length=30, default='', db_index=True, unique=True, verbose_name='фрегат id')
    phone = models.CharField(max_length=255, blank=True, verbose_name='телефон')
    mail = models.CharField(max_length=255, null=True, blank=True, verbose_name='E-mail')
    fed_region = models.ForeignKey(FedRegion, models.SET_NULL, null=True, default=None,
                                   verbose_name='федеральный округ')

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
