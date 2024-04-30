import datetime

from django.core.files.storage import FileSystemStorage
from django.db import models

from maket5_0.models import Order, OrderItem, OrderPrint, PrintType, PrintPlace, PrintPosition

fs_maket = FileSystemStorage(location='maket5_0/files/maket')


class Maket(models.Model):
    date_create = models.DateField(blank=True, default=datetime.date.today)
    date_modified = models.DateField(blank=True, default=datetime.date.today)
    maket_number = models.SmallIntegerField(default=1)
    uploaded = models.BooleanField(default=False)
    file = models.FileField(storage=fs_maket, null=True, blank=True)
    comment = models.CharField(max_length=255, default='')
    order = models.ForeignKey(Order, models.SET_NULL, null=True)
    order_number = models.CharField(max_length=40, blank=True, null=True)
    order_date = models.DateField(default='2024-01-01')
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "макет"
        verbose_name_plural = "макеты"
        ordering = ['-order_number', 'maket_number']
        db_table_comment = 'Maket'
        db_table = 'maket'

    def __repr__(self):
        return self.order_number

    def __str__(self):
        return str(self.order_number + ' ' + self.order.customer.name)

    @staticmethod
    def order_default():
        return ['-order_number', 'maket_number']


class MaketItem(models.Model):
    """If item from order exists in Maket"""
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    maket = models.ForeignKey(Maket, on_delete=models.CASCADE, null=True, blank=True)
    checked = models.BooleanField(default=True)
    print_name = models.CharField(max_length=50,  null=True, blank=True)

    class Meta:
        verbose_name = "состав макета"
        verbose_name_plural = "составы макетов"
        db_table_comment = 'MaketItem'
        db_table = 'maket_item'

    def __repr__(self):
        return str(self.maket.order_number + ' ' + self.item.item.article)

    def __str__(self):
        return str(self.maket.order_number + ' ' + self.item.item.article)


class MaketPrint(models.Model):
    """If print item shows big in Maket"""
    print_item = models.ForeignKey(OrderPrint, models.SET_NULL, null=True, blank=True)
    maket = models.ForeignKey(Maket, on_delete=models.CASCADE, null=True, blank=True)
    checked = models.BooleanField(default=True)
    print_type = models.ForeignKey(PrintType, models.SET_NULL, null=True, blank=True)
    print_place = models.ForeignKey(PrintPlace, models.SET_NULL, null=True, blank=True)
    print_position = models.ForeignKey(PrintPosition, models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "печать в макете"
        verbose_name_plural = "печать в макетах"
        db_table_comment = 'MaketPrint'
        db_table = 'maket_print'

    def __str__(self):
        return self.print_item.item.item.name + ' ' + self.print_item.item.print_name

    def __repr__(self):
        return self.print_item.item.item.name + ' ' + self.print_item.item.print_name
