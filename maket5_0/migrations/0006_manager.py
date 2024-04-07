# Generated by Django 5.0.3 on 2024-04-07 20:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket5_0', '0005_detailtype_alter_printplace_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('phone', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('mail', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('customer_group', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.customergroup')),
            ],
            options={
                'verbose_name': 'Менеджер клиента',
                'verbose_name_plural': 'Менеджеры клиентов',
                'db_table': 'manager',
                'db_table_comment': 'Manager',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
    ]
