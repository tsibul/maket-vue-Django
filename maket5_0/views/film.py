import datetime

from django.db.models import Q, Func, Value, F
from django.forms import CharField
from django.http import JsonResponse
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Film, MaketGroup, GroupInFilm


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def film_list_for_group(request, group_id, connected):
    """

    :param request: film_list_for_group/<int:group_id>/<int:connected>
    :param group_id:
    :param connected:
    :return:
    """
    if connected:
        film_list = Film.objects.filter(groupinfilm__group__id=group_id, deleted=False).order_by('-date')
    else:
        film_list = Film.objects.filter(~Q(groupinfilm__group__id=group_id) & Q(deleted=False)).order_by('-date')
    # film_list = Film.objects.filter(groupinfilm__group__id=group_id, deleted=False).order_by('-date')
    film_list_out = film_list.annotate(
        dateCreate=Func(
            F('date'),
            Value('DD.MM.YY'),
            function='to_char',
            output_field=CharField()
        ),
        dateSent=Func(
            F('date_sent'),
            Value('DD.MM.YY'),
            function='to_char',
            output_field=CharField()
        ),
    ).values(
        'film_number',
        'dateCreate',
        'dateSent',
        'status',
        'groupinfilm__id',
    )
    return JsonResponse(list(film_list_out), safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def group_to_film(request, group_id, film_id):
    """
    Connect maket_group to film through group_in_film
    :param request: group_to_film/<int:group_id>/<int:film_id>
    :param group_id:
    :param film_id:
    :return: connected film data
    """
    maket_group = MaketGroup.objects.get(id=group_id)
    if film_id:
        film = Film.objects.get(id=film_id)
    else:
        film_last = Film.objects.all().order_by('-date').first()
        film_number = film_last.film_number + 1 if film_last else 1
        film = Film(film_number=film_number, date=datetime.date.today())
        film.save()
    group_in_film = GroupInFilm.objects.filter(group=maket_group, film=film).first()
    if not group_in_film:
        group_in_film = GroupInFilm(group=maket_group, film=film)
    group_in_film.status = True
    group_in_film.save()
    film_data = {
        'film_number': film.film_number,
        'dateCreate': film.date.strftime('%d.%m.%y'),
        'dateSent': film.date_sent.strftime('%d.%m.%y'),
        'status': film.status,
        'groupinfilm__id': group_in_film.id,

    }
    return JsonResponse(film_data, safe=False)