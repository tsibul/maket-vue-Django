# Generated by Django 5.0.4 on 2024-04-14 05:52

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maket5_0', '0007_order_orderitem_orderprint_printcolor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='customer_address',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='inn',
            new_name='customer_inn',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='name',
            new_name='customer_name',
        ),
        migrations.AddField(
            model_name='order',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='version',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]