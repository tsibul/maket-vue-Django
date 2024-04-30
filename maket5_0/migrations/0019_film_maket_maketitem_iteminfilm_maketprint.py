# Generated by Django 5.0.4 on 2024-04-30 15:42

import datetime
import django.core.files.storage
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket5_0', '0018_pantonetohex_alter_orderitem_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film_number', models.IntegerField(default=0)),
                ('date', models.DateField(blank=True, default='')),
                ('format', models.CharField(default='A5', max_length=3)),
                ('status', models.BooleanField(default=False)),
                ('date_sent', models.DateField(default=None, null=True)),
                ('film_upload', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='maket_0/files/film'), upload_to='')),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'пленка',
                'verbose_name_plural': 'пленки',
                'db_table': 'film',
                'db_table_comment': 'Film',
                'ordering': ['-date', '-film_number'],
            },
        ),
        migrations.CreateModel(
            name='Maket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateField(blank=True, default=datetime.date.today)),
                ('date_modified', models.DateField(blank=True, default=datetime.date.today)),
                ('maket_number', models.SmallIntegerField(default=1)),
                ('uploaded', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='maket5_0/files/maket'), upload_to='')),
                ('comment', models.CharField(default='', max_length=255)),
                ('order_number', models.CharField(blank=True, max_length=40, null=True)),
                ('order_date', models.DateField(default='2024-01-01')),
                ('deleted', models.BooleanField(default=False)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.order')),
            ],
            options={
                'verbose_name': 'макет',
                'verbose_name_plural': 'макеты',
                'db_table': 'maket',
                'db_table_comment': 'Maket',
                'ordering': ['-order_number', 'maket_number'],
            },
        ),
        migrations.CreateModel(
            name='MaketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked', models.BooleanField(default=True)),
                ('print_name', models.CharField(blank=True, max_length=50, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maket5_0.orderitem')),
                ('maket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maket5_0.maket')),
            ],
            options={
                'verbose_name': 'состав макета',
                'verbose_name_plural': 'составы макетов',
                'db_table': 'maket_item',
                'db_table_comment': 'MaketItem',
            },
        ),
        migrations.CreateModel(
            name='ItemInFilm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('print_name', models.CharField(default='', max_length=255)),
                ('status', models.BooleanField(default=True)),
                ('film', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.film')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.maketitem')),
            ],
            options={
                'verbose_name': 'нанесение на пленке',
                'verbose_name_plural': 'нанесения на пленках',
                'db_table': 'item-in-film',
                'db_table_comment': 'ItemInFilm',
                'ordering': ['-film__date', '-film__film_number', 'print_name'],
            },
        ),
        migrations.CreateModel(
            name='MaketPrint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked', models.BooleanField(default=True)),
                ('maket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='maket5_0.maket')),
                ('print_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.orderprint')),
                ('print_place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.printplace')),
                ('print_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.printposition')),
                ('print_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.printtype')),
            ],
            options={
                'verbose_name': 'печать в макете',
                'verbose_name_plural': 'печать в макетах',
                'db_table': 'maket_print',
                'db_table_comment': 'MaketPrint',
            },
        ),
    ]
