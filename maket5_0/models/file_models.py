import pathlib
from django.db import models
from django.core.files.storage import FileSystemStorage

from maket5_0.models import SettingsDictionary, Order

fs_additional = FileSystemStorage(location='maket5_0/files/additional')


class AdditionalFile(SettingsDictionary):
    """Additional files"""
    additional_file = models.FileField(storage=fs_additional, null=True, blank=True)
    additional_file_name = models.FilePathField(max_length=255)
    file_type = models.CharField(max_length=8, null=True, blank=True, default='pdf')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta(SettingsDictionary.Meta):
        verbose_name = "файл"
        verbose_name_plural = "файлы"
        ordering = ['-order__order_date', 'order__order_number']
        db_table_comment = 'AdditionalFile'
        db_table = 'additional_file'

    def save(self, *args, **kwargs):
        self.file_type = pathlib.Path(str(self.additional_file_name)).suffix
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + ' ' + self.additional_file_name

    def __repr__(self):
        return self.name + ' ' + self.additional_file_name

    @staticmethod
    def order_default():
        return ['-order__order_date', 'order__order_number']

