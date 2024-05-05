from django.core.files.storage import FileSystemStorage
from django.db import models

from maket5_0.models import SettingsDictionary, Good, MaterialType, PrintPosition

fs_detail_images = FileSystemStorage(location='files/detail_images')


class GoodsImagesSet(SettingsDictionary):
    """Set of Images of each detail
    images_quantity — size of images set"""
    good = models.ForeignKey(Good, on_delete=models.CASCADE, null=True, blank=True)
    images_quantity = models.IntegerField(verbose_name='количество изображений элемента')

    class Meta(SettingsDictionary.Meta):
        verbose_name = 'Набор изображений изделия'
        verbose_name_plural = 'Наборы изображений изделий'
        db_table_comment = 'Set of Goods Images'
        db_table = 'goods_images_set'

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = str(self.good.name)
        super(GoodsImagesSet, self).save(*args, **kwargs)

    @staticmethod
    def dictionary_fields():
        return [
            {
                'field': 'good',
                'type': 'foreign',
                'label': 'продукция',
                'foreignClass': 'Good'
            },
            {
                'field': 'images_quantity',
                'type': 'string',
                'label': 'кол-во видов',
                'number': True,
                'null': False,
                'emitChoices': True
            },
        ]


class DetailImage(SettingsDictionary):
    """Image for Detail"""
    goods_image_set = models.ForeignKey(GoodsImagesSet, on_delete=models.CASCADE,
                                         verbose_name='набор изображений', null=True, blank=True)
    image_number = models.IntegerField(choices=[], verbose_name='порядковый номер')
    print_position = models.ForeignKey(PrintPosition, models.SET_NULL, verbose_name='место нанесения', null=True)
    svg_file = models.FileField(storage=fs_detail_images, null=True, blank=True, verbose_name='файл изображения')

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
                'choices': 'detailI_mages_set',
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
