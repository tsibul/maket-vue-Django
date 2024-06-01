import datetime

from django.db import models
from django.core.files.storage import FileSystemStorage

from maket5_0.models.maket_models import MaketItem, MaketGroup

fs_film = FileSystemStorage(location='maket_0/files/film')


class Film(models.Model):
    film_number = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today, blank=True)
    format = models.CharField(max_length=3, default='A5')
    status = models.BooleanField(default=False)
    date_sent = models.DateField(default=None, null=True)
    file = models.FileField(storage=fs_film, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "пленка"
        verbose_name_plural = "пленки"
        ordering = ['-date', '-film_number']
        db_table_comment = 'Film'
        db_table = 'film'

    def __repr__(self):
        return str(self.film_number) + ' от ' + str(self.date)

    def __str__(self):
        return str(self.film_number) + ' от ' + str(self.date)

    @staticmethod
    def order_default():
        return ['-date', '-film_number']


class ItemInFilm(models.Model):
    """If item correctly output in film"""
    item = models.ForeignKey(MaketItem, models.SET_NULL, null=True, blank=True)
    film = models.ForeignKey(Film, models.SET_NULL, null=True, blank=True)
    print_name = models.CharField(max_length=255, default='')
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "нанесение на пленке"
        verbose_name_plural = "нанесения на пленках"
        ordering = ['-film__date', '-film__film_number', 'print_name']
        db_table_comment = 'ItemInFilm'
        db_table = 'item-in-film'


class GroupInFilm(models.Model):
    """If group correctly output in film"""
    group = models.ForeignKey(MaketGroup, models.SET_NULL, null=True, blank=True)
    film = models.ForeignKey(Film, models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "нанесение на пленке"
        verbose_name_plural = "нанесения на пленках"
        ordering = ['-film__date', '-film__film_number', 'group__name']
        db_table_comment = 'GroupInFilm'
        db_table = 'group-in-film'
