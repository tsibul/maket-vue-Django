# Generated by Django 5.0.4 on 2024-04-16 05:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket5_0', '0010_alter_orderitem_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderprint',
            name='print_type',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.printtype'),
        ),
    ]
