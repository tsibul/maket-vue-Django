import datetime

from django.db.models import Q, Func, Value, F, CharField
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Film, MaketGroup, GroupInFilm, OrderItem, OrderPrint
from maket5_0.views.search_filters import film_search_filter


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def film_list_for_group(request, group_id, connected):
    """

    :param request: film_list_for_group/<int:group_id>/<int:connected>
    :param group_id:
    :param connected:
    :return:
    """
    film_list = Film.objects.filter(deleted=False)
    if not connected:
        film_list = film_list.filter(
            groupinfilm__group__id=group_id,
            groupinfilm__deleted=False,
        ).order_by(
            '-date',
            '-film_number'
        )
    else:
        film_list = film_list.filter(
            (
                    ~Q(groupinfilm__group__id=group_id)
                    |
                    Q(groupinfilm__deleted=True)
                    &
                    Q(groupinfilm__group__id=group_id)
            ) &
            Q(deleted=False)).order_by(
            '-date',
            '-film_number'
        ).distinct()
    # film_list = Film.objects.filter(groupinfilm__group__id=group_id, deleted=False).order_by('-date')
    film_list_out = list(film_list.annotate(
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
        'id',
        'film_number',
        'dateCreate',
        'dateSent',
        'status',
    ))
    return JsonResponse(film_list_out, safe=False)


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
    group_in_film.deleted = False
    group_in_film.save()
    film_data = film_data_for_group(film, group_in_film)
    return JsonResponse(film_data, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def group_from_film(request, group_id, film_id):
    """
    Remove group from film through group_in_film
    :param request: roup_from_film/<int:group_id>/<int:film_id>
    :param group_id:
    :param film_id:
    :return: disconnected film data
    """
    maket_group = MaketGroup.objects.get(id=group_id)
    film = Film.objects.get(id=film_id)
    group_in_film = GroupInFilm.objects.filter(group=maket_group, film=film).first()
    group_in_film.deleted = True
    group_in_film.save()
    film_data = film_data_for_group(film, group_in_film)
    return JsonResponse(film_data, safe=False)


def film_data_for_group(film, group_in_film):
    return {
        'id': film.id,
        'film_number': film.film_number,
        'dateCreate': film.date.strftime('%d.%m.%y'),
        'dateSent': film.date_sent.strftime('%d.%m.%y') if film.date_sent else None,
        'status': film.status,
        'groupinfilm__id': group_in_film.id,
    }


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def film_list_info(request, search_string, sh_deleted, id_no):
    """
    Form film list
    :param request: film_list/<str:search_string>/<int:sh_deleted>/<int:id_no>
    :param search_string:
    :param sh_deleted:
    :param id_no:
    :return:
    """
    film_list = Film.objects.all()
    if not sh_deleted:
        film_list = film_list.filter(deleted=False)
    if search_string != 'default':
        film_list = film_search_filter(film_list, search_string, sh_deleted)
    film_list = film_list.order_by('-date', '-film_number')[id_no: id_no + 20]
    film_list_out = []
    for film in film_list:
        groups_in_film = GroupInFilm.objects.filter(film=film)
        if not sh_deleted:
            groups_in_film =  groups_in_film.filter(deleted=False)
        groups = []
        for group in groups_in_film:
            order_item = OrderItem.objects.filter(order=group.group.maket.order, item_group=group.group.name).first()
            print_type = OrderPrint.objects.filter(item=order_item).first().print_type.name
            group = {
                'id': group.id,
                'item': group.group.name.split('()')[0],
                'printName': group.group.name.split('()')[1],
                'maketNumber': group.group.maket.maket_number,
                'orderNumber': group.group.maket.order.order_number,
                'orderDate': group.group.maket.order.order_date.strftime('%d.%m.%y'),
                'customer': group.group.maket.order.customer.name,
                'printType': print_type,
                'comment': group.comment,
                'status': group.status,
                'deleted': group.deleted,
            }
            groups.append(group)
        single_film = {
            'id': film.id,
            'filmNumber': film.film_number,
            'dateCreate': film.date.strftime('%d.%m.%y'),
            'dateSent': film.date_sent.strftime('%d.%m.%y') if film.date_sent else None,
            'format': film.format,
            'file': film.file.name,
            'status': film.status,
            'groups': groups,
        }
        film_list_out.append(single_film)
    return JsonResponse(film_list_out, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def toggle_film_status(request, film_id):
    """
    Change film status
    :param request: toggle_film_status/<int:film_id>
    :param film_id:
    :return:
    """
    film = GroupInFilm.objects.get(id=film_id)
    film.status = not film.status
    film.save()
    return JsonResponse(film.id, safe=False)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def set_film_comment(request, film_id):
    """
    Set film in group comment
    :param request: set_film_comment/<int:film_id>
    :param film_id:
    :return:
    """
    group = GroupInFilm.objects.get(id=film_id)
    comment = request.data['comment']
    group.comment = comment
    group.save()
    return JsonResponse({'id': group.id}, safe=False)