# Generated by Django 5.0.4 on 2024-05-05 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket5_0', '0024_maketpattern_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='maket_pattern',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.maketpattern', verbose_name='размещение в макете'),
        ),
    ]
