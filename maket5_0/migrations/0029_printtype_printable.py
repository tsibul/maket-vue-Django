# Generated by Django 5.0.4 on 2024-05-06 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket5_0', '0028_good_goods_images_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='printtype',
            name='printable',
            field=models.BooleanField(default=True),
        ),
    ]