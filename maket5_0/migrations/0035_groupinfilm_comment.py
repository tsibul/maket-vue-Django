# Generated by Django 5.0.4 on 2024-06-05 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket5_0', '0034_remove_film_film_upload_alter_film_date_groupinfilm'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupinfilm',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]