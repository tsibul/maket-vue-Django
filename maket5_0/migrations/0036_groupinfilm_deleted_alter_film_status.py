# Generated by Django 5.0.4 on 2024-06-05 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket5_0', '0035_groupinfilm_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupinfilm',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='film',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
