from django.core.files.storage import FileSystemStorage
from django.db import models

from maket5_0.models import SettingsDictionary, Good, MaterialType, PrintPosition

fs_detail_images = FileSystemStorage(location='files/detail_images')


class DetailImagesSet(SettingsDictionary):
    """Set of Images of each detail
    images_quantity — size of images set"""
    images_quantity = models.IntegerField(verbose_name='количество изображений элемента')

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Набор изображений детали'
        verbose_name_plural = 'Наборы изображений детали'
        db_table_comment = 'Set of Detail Images'
        db_table = 'detail_images_set'

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'images_quantity',
                'type': 'string',
                'label': 'кол-во видов',
                'number': True,
                'null': False,
                'emitChoices': True
            },
        ]


class DetailItem(SettingsDictionary):
    """Article item
    attributes_group_type — color scheme type
    item_position — position of item in article (divided by '.')
    item_position_in_image — position of item in good picture
    images_quantity - number of view variants for item"""
    material_type = models.ForeignKey(MaterialType, on_delete=models.SET_NULL, null=True)
    good = models.ForeignKey(Good, on_delete=models.CASCADE, verbose_name='продукция')
    detail_images_set = models.ForeignKey(DetailImagesSet, models.SET_NULL, null=True, verbose_name='набор изображений',
                                          blank=True)
    item_position = models.IntegerField(choices=[], verbose_name='позиция группы артикула')
    item_position_in_image = models.IntegerField(choices=[], verbose_name='позиция в сборке')
    for_printing = models.BooleanField(default=True, verbose_name='нанесение')

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Элемент артикула'
        verbose_name_plural = 'Элементы артикула'
        db_table_comment = 'Article Item'
        db_table = 'article_item'
        ordering = ['good', 'item_position']

    # def __init__(self, *args, **kwargs):
    #     super(DetailItem, self).__init__(*args, **kwargs)
    #     if self.good:
    #         good = Good.objects.get(pk=self.good.pk)
    #         choices = [(i, str(i)) for i in range(0, good.detail_quantity + 1)]
    #         self._meta.get_field('item_position').choices = choices
    #         self._meta.get_field('item_position_in_image').choices = choices

    def save(self, *args, **kwargs):
        if self.good:
            good = Good.objects.get(pk=self.good.pk)
            choices = [(i, str(i)) for i in range(0, good.detail_quantity + 1)]
            self._meta.get_field('item_position').choices = choices
            self._meta.get_field('item_position_in_image').choices = choices
        super(DetailItem, self).save(*args, **kwargs)

    @staticmethod
    def order_default():
        return ['good', 'item_position']

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'material_type',
                'type': 'foreign',
                'label': 'тип материала',
                'foreignClass': 'MaterialType',
                'null': False
            },
            {
                'field': 'good',
                'type': 'foreign',
                'label': 'продукция',
                'foreignClass': 'Good',
                'null': False
            },
            {
                'field': 'detail_images_set',
                'type': 'foreign',
                'label': 'набор видов',
                'foreignClass': 'DetailImagesSet'
            },
            {
                'field': 'item_position',
                'type': 'choices',
                'label': 'позиция группы',
                'choices': 'Good',
                'choicesField': 'detail_quantity',
                'null': False
            },
            {
                'field': 'item_position_in_image',
                'type': 'choices',
                'label': 'позиция в виде',
                'choices': 'Good',
                'choicesField': 'detail_quantity',
                'null': False
            },
            {
                'field': 'for_printing',
                'type': 'boolean',
                'label': 'нанесение',
                'null': False
            },
        ]


class DetailImage(SettingsDictionary):
    """Image for Detail"""
    detail_image_set = models.ForeignKey(DetailImagesSet, on_delete=models.CASCADE,
                                         verbose_name='набор изображений')
    image_number = models.IntegerField(choices=[], verbose_name='порядковый номер')
    print_position = models.ForeignKey(PrintPosition, models.SET_NULL, verbose_name='место нанесения', null=True)
    svg_file = models.FileField(storage=fs_detail_images, null=True, blank=True, verbose_name='файл изображения')

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'SVG код элемента'
        verbose_name_plural = 'SVG код элементов'
        db_table_comment = 'SVG Detail code'
        db_table = 'detail_image'
        ordering = ['detail_image_set', 'image_number']

    # def __init__(self, *args, **kwargs):
    #     super(DetailImage, self).__init__(*args, **kwargs)
    #     if self.detail_image_set:
    #         detail_image_set = DetailImagesSet.objects.get(pk=self.detail_image_set.pk)
    #         choices = [(i, str(i)) for i in range(0, detail_image_set.images_quantity + 1)]
    #         self._meta.get_field('image_number').choices = choices

    def save(self, *args, **kwargs):
        if self.detail_image_set:
            detail_image_set = DetailImagesSet.objects.get(pk=self.detail_image_set.pk)
            choices = [(i, str(i)) for i in range(0, detail_image_set.images_quantity + 1)]
            self._meta.get_field('image_number').choices = choices
        super(DetailImage, self).save(*args, **kwargs)

    @staticmethod
    def order_default():
        return ['detail_image_set', 'image_number']

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'detail_image_set',
                'type': 'foreign',
                'label': 'набор изображений',
                'foreignClass': 'DetailImagesSet'
            },
            {
                'field': 'image_number',
                'type': 'choices',
                'label': 'порядковый номер',
                'choices': 'DetailImagesSet',
                'choicesField': 'images_quantity'
            },
            {
                'field': 'print_position',
                'type': 'foreign',
                'label': 'место нанесения',
                'foreignClass': 'PrintPosition'
            },
            {
                'field': 'svg_file',
                'type': 'svgFile',
                'label': 'файл изображения',
            },
        ]
