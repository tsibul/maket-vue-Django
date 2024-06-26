# Generated by Django 5.0.3 on 2024-03-09 14:13

import django.core.files.storage
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ColorScheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
            ],
            options={
                'verbose_name': 'Цветовая схема',
                'verbose_name_plural': 'Цветовые схемы',
                'db_table': 'color_scheme',
                'db_table_comment': 'Color Scheme (Grant, TetraPak, Italiano Vero etc)',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('phone', models.CharField(default='', max_length=255, verbose_name='телефон')),
                ('mail', models.CharField(default='', max_length=255, verbose_name='E-mail')),
                ('default', models.BooleanField(default=True, verbose_name='стандарт')),
            ],
            options={
                'verbose_name': 'Группа клиентов',
                'verbose_name_plural': 'Группы клиентов',
                'db_table': 'customer_group',
                'db_table_comment': 'Customer Group',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('group_discount', models.FloatField(default=0, verbose_name='скидка')),
                ('code', models.CharField(default='', max_length=2, verbose_name='код группы')),
            ],
            options={
                'verbose_name': 'Тип клиента',
                'verbose_name_plural': 'Типы клиентов',
                'db_table': 'customer_type',
                'db_table_comment': 'Customer Type',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DetailImagesSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('images_quantity', models.IntegerField(verbose_name='количество изображений элемента')),
            ],
            options={
                'verbose_name': 'Набор изображений детали',
                'verbose_name_plural': 'Наборы изображений детали',
                'db_table': 'detail_images_set',
                'db_table_comment': 'Set of Detail Images',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FedRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
            ],
            options={
                'verbose_name': 'Федеральный округ',
                'verbose_name_plural': 'Федеральные округа',
                'db_table': 'fed_region',
                'db_table_comment': 'Federal Region Model',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MaterialType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Типы материала',
                'db_table': 'material_type',
                'db_table_comment': 'Material Type (plastic, metal, paper, block printing etc)',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrintPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
            ],
            options={
                'verbose_name': 'место нанесения',
                'verbose_name_plural': 'места нанесения',
                'db_table': 'print_place',
                'db_table_comment': 'Print Place',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrintPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
            ],
            options={
                'verbose_name': 'положение нанесения',
                'verbose_name_plural': 'положения печати',
                'db_table': 'print_position',
                'db_table_comment': 'Print Position',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PrintType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
            ],
            options={
                'verbose_name': 'тип печати',
                'verbose_name_plural': 'типы печати',
                'db_table': 'print_type',
                'db_table_comment': 'Print Type',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TypeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
            ],
            options={
                'verbose_name': 'Тип группы',
                'verbose_name_plural': 'Типы групп',
                'db_table': 'type_group',
                'db_table_comment': 'Group Type',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='код')),
                ('pantone', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='PANTONE')),
                ('hex', models.CharField(blank=True, max_length=7, null=True, verbose_name='HEX')),
                ('standard', models.BooleanField(default=True, verbose_name='стандарт')),
                ('color_scheme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.colorscheme', verbose_name='цветовая схема')),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
                'db_table': 'color',
                'db_table_comment': 'Color',
                'ordering': ['color_scheme', 'code'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerGroupFrigateId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frigate_code', models.CharField(max_length=30, unique=True, verbose_name='фрегат id')),
                ('customer_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket5_0.customergroup', verbose_name='группа клиентов')),
            ],
            options={
                'verbose_name': 'Группа клиентов',
                'verbose_name_plural': 'Группы клиентов',
                'db_table': 'customer_group_frigate_id',
                'db_table_comment': 'Customer Group Frigate ID',
            },
        ),
        migrations.AddField(
            model_name='customergroup',
            name='customer_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.customertype', verbose_name='тип клиента'),
        ),
        migrations.AddField(
            model_name='customergroup',
            name='fed_region',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.fedregion', verbose_name='федеральный округ'),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.CharField(blank=True, max_length=255, verbose_name='форма')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='адрес')),
                ('inn', models.CharField(max_length=20, null=True, verbose_name='ИНН')),
                ('region', models.CharField(max_length=2, verbose_name='регион')),
                ('frigate_code', models.CharField(db_index=True, default='', max_length=30, unique=True, verbose_name='фрегат id')),
                ('phone', models.CharField(blank=True, max_length=255, verbose_name='телефон')),
                ('mail', models.CharField(blank=True, max_length=255, null=True, verbose_name='E-mail')),
                ('customer_group', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.customergroup', verbose_name='группа клиентов')),
                ('customer_type', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.customertype', verbose_name='тип клиента')),
                ('fed_region', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.fedregion', verbose_name='федеральный округ')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'db_table': 'customer',
                'db_table_comment': 'Customer',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('article', models.CharField(blank=True, max_length=30, null=True)),
                ('detail_quantity', models.SmallIntegerField(default=1)),
                ('color_scheme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.colorscheme')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
                'db_table': 'goods',
                'db_table_comment': 'Goods',
                'ordering': ['article'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DetailItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('item_position', models.IntegerField(choices=[], verbose_name='позиция группы артикула')),
                ('item_position_in_image', models.IntegerField(choices=[], verbose_name='позиция в сборке')),
                ('for_printing', models.BooleanField(default=True, verbose_name='нанесение')),
                ('detail_images_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.detailimagesset', verbose_name='набор изображений')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket5_0.good', verbose_name='продукция')),
                ('material_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.materialtype')),
            ],
            options={
                'verbose_name': 'Элемент артикула',
                'verbose_name_plural': 'Элементы артикула',
                'db_table': 'article_item',
                'db_table_comment': 'Article Item',
                'ordering': ['good', 'item_position'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='colorscheme',
            name='color_scheme_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.materialtype', verbose_name='материал'),
        ),
        migrations.CreateModel(
            name='DetailImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('image_number', models.IntegerField(choices=[], verbose_name='порядковый номер')),
                ('svg_file', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='files/detail_images'), upload_to='', verbose_name='файл изображения')),
                ('detail_image_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket5_0.detailimagesset', verbose_name='набор изображений')),
                ('print_position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.printposition', verbose_name='место нанесения')),
            ],
            options={
                'verbose_name': 'SVG код элемента',
                'verbose_name_plural': 'SVG код элементов',
                'db_table': 'detail_image',
                'db_table_comment': 'SVG Detail code',
                'ordering': ['detail_image_set', 'image_number'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegionToFedRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140, verbose_name='название')),
                ('deleted', models.BooleanField(default=False, verbose_name='удалено')),
                ('fed_region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maket5_0.fedregion', verbose_name='федеральный округ')),
            ],
            options={
                'verbose_name': 'Соответствие ИНН и федерального округа',
                'verbose_name_plural': 'Соответствие ИНН и федерального округов',
                'db_table': 'region_to_fed_region',
                'db_table_comment': 'Region to Federal Region correspondence',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='customertype',
            name='type_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='maket5_0.typegroup', verbose_name='тип группы'),
        ),
    ]
