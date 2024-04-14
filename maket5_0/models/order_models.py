import datetime

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

from maket5_0.models import Customer, Manager, Good, PrintPlace, PrintPosition, TypeGroup, CustomerType, CustomerGroup

fs_orders = FileSystemStorage(location='files/orders')


class Order(models.Model):
    """
    Order model
    """
    order_number = models.CharField(max_length=18, blank=True, null=True)
    order_date = models.DateField(default='1000-01-01')
    supplier = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_inn = models.CharField(max_length=12, blank=True, null=True)
    customer_address = models.CharField(max_length=255, blank=True, null=True)
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    order_quantity = models.IntegerField(default=0)
    order_sum = models.FloatField(default=0)
    print_quantity = models.IntegerField(default=0)
    print_sum = models.FloatField(default=0)
    our_manager = models.CharField(max_length=50, blank=True, null=True, default='')
    manager = models.ForeignKey(Manager, models.SET_NULL, blank=True, null=True, default='')
    Ready = 'R'
    Partial = 'P'
    NotReady = 'N'
    status_choices = [(Ready, 'R'), (Partial, 'P'), (NotReady, 'N')]
    maket_status = models.CharField(max_length=1, choices=status_choices, default=NotReady)
    order_upload = models.BooleanField(default=False)
    order_file = models.FileField(storage=fs_orders, null=True, blank=True)
    to_check = models.BooleanField(default=False)
    number_orders = models.SmallIntegerField(default=0)
    number_makets = models.SmallIntegerField(default=0)
    number_additional = models.SmallIntegerField(default=0)
    deleted = models.BooleanField(default=False)
    version = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table_comment = 'Order'
        db_table = 'order'

    def __repr__(self):
        return self.order_number

    def __str__(self):
        return str(self.order_number + ' ' + self.customer.name)

    def order_from_parse(self, tr_strings):
        if len(tr_strings) > 0:
            self.order_number = str(tr_strings[2][0])
            self.order_date = datetime.datetime.strptime(tr_strings[1][0], '%d.%m.%Y').date()
            self.supplier = str(tr_strings[4][0])
            self.customer_name = str(tr_strings[6][0])
            self.customer_inn = str(tr_strings[7][0])
            self.customer_address = str(tr_strings[8][0])
            self.order_quantity = int(str(tr_strings[10][0]))
            self.order_sum = float((str(tr_strings[12][0])).replace(',', '.'))
            self.our_manager = str(tr_strings[13][0])

    def update_customer_for_import_order(self):
        inn = self.customer_inn
        if inn and Customer.objects.filter(inn=inn).order_by('id').last():
            customer = Customer.objects.filter(inn=inn).order_by('id').last()
            if self.customer_name != customer.name:
                customer.name = self.customer_name
                customer.save()
        else:
            customer_type_import = self.order_number[slice(13, 15)]
            customer_type = CustomerType.objects.filter(code=customer_type_import).first()
            type_group = None
            if customer_type:
                type_group = customer_type.type_group
            customer = Customer.objects.filter(customer_type__type_group=type_group, name=self.customer_name).order_by(
                'id').last()
            if not customer:
                customer_type = CustomerType.objects.get(type_group=type_group)
                customer = Customer(name=self.customer_name, inn=self.customer_inn, address=self.customer_address,
                                    customer_type=customer_type)
                group = CustomerGroup()
                group.default_group(customer)
                group.save()
                customer.customer_group = group
                customer.save()
        self.customer = customer


class OrderItem(models.Model):
    """
    Order Item model
    """
    print_no = models.IntegerField(default=0)
    item = models.ForeignKey(Good, models.SET_NULL, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    print_name = models.CharField(max_length=50, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    item_price = models.FloatField(default=0)
    print_price = models.FloatField(default=0)
    num_prints = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Номенклатура заказа'
        verbose_name_plural = 'Номенклатура заказов'
        db_table_comment = 'OrderItem'
        db_table = 'order_item'

    def __repr__(self):
        return self.code + ' ' + self.print_name

    def __str__(self):
        return str(self.code + ' ' + self.print_name)


class OrderPrint(models.Model):
    """
    Order Print model
    """
    place = models.CharField(max_length=30, blank=True, null=True)
    print_place = models.ForeignKey(PrintPlace, models.SET_NULL, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    colors = models.SmallIntegerField(default=1)
    second_pass = models.BooleanField(default=False)
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True)
    print_no = models.IntegerField(default=0)
    print_price = models.FloatField(default=0)
    print_position = models.ForeignKey(PrintPosition, models.SET_NULL, null=True, default='')

    class Meta:
        verbose_name = 'Нанесение'
        verbose_name_plural = 'Нанесения'
        db_table_comment = 'OrderPrint'
        db_table = 'order_print'


class PrintColor(models.Model):
    """Colors of printing"""
    pantone = models.CharField(max_length=40, default='')
    hex = models.CharField(max_length=7, default='')
    number_in_item = models.SmallIntegerField(default=1)
    print_item = models.ForeignKey(OrderPrint, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Цвет нанесения'
        verbose_name_plural = 'Цвета нанесения'
        db_table_comment = 'PrintColor'
        db_table = 'print_color'

    def __repr__(self):
        return str(self.number_in_item) + ' ' + self.pantone

    def __str__(self):
        return str(self.number_in_item) + ' ' + self.pantone
