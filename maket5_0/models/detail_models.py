from django.core.files.storage import FileSystemStorage
from django.db import models

from maket5_0.models import SettingsDictionary, PrintPosition, GoodsImagesSet

fs_detail_images = FileSystemStorage(location='maket5_0/files/detail_images')


class DetailImage(SettingsDictionary):
    """Image for Detail"""
    goods_image_set = models.ForeignKey(GoodsImagesSet, on_delete=models.CASCADE,
                                         verbose_name='набор изображений', null=True, blank=True)
    image_number = models.IntegerField(choices=[], verbose_name='порядковый номер')
    print_position = models.ForeignKey(PrintPosition, models.SET_NULL, verbose_name='место нанесения', null=True)
    svg_file = models.FileField(storage=fs_detail_images, null=True, blank=True, verbose_name='файл изображения')
    image_width = models.FloatField(default=138.205, null=True, blank=True)

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'SVG код элемента'
        verbose_name_plural = 'SVG код элементов'
        db_table_comment = 'SVG Detail code'
        db_table = 'detail_image'
        ordering = ['goods_image_set', 'image_number']

    def save(self, *args, **kwargs):
        if self.goods_image_set:
            detail_image_set = GoodsImagesSet.objects.get(pk=self.goods_image_set.pk)
            choices = [(i, str(i)) for i in range(0, detail_image_set.images_quantity + 1)]
            self._meta.get_field('image_number').choices = choices
        super(DetailImage, self).save(*args, **kwargs)

    @staticmethod
    def order_default():
        return ['goods_image_set', 'image_number']

    @staticmethod
    def dictionary_fields():
        return [
            SettingsDictionary.dictionary_fields()[0],
            {
                'field': 'goods_image_set',
                'type': 'foreign',
                'label': 'набор изображений',
                'foreignClass': 'GoodsImagesSet'
            },
            {
                'field': 'image_number',
                'type': 'choices',
                'label': 'порядковый номер',
                'choices': 'goods_image_set',
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
                'type': 'file',
                'label': 'файл изображения',
            },
            {
                'field': 'image_width',
                'type': 'string',
                'label': 'длина изображения',
                'number': True,
            },
        ]
