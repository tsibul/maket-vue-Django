import os

from django.core.files import File
from django.db.models import Count, Q, CharField, Value, F, Func
from django.http import JsonResponse, FileResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Maket, Order, MaketGroup, Film
from maket5_0.views import order_search_filter


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_list_info(request, search_string, sh_deleted, id_no):
    order_list = Order.objects.filter(
        maket__isnull=False
    )
    if not sh_deleted:
        order_list = order_list.filter(deleted=False, maket__deleted=False)
    if search_string != 'default':
        order_list = order_search_filter(order_list, search_string)
    order_list = order_list.order_by('-order_date', '-order_number')[id_no: id_no + 20]
    order_list = order_list.values(
        'id',
        'maket_status',
        'order_number',
        'order_date',
        'customer__name',
        'maket__id',
        'maket__maket_number',
        'maket__date_create',
        'maket__comment',
        'maket__file',
        'maket__deleted'
    ).annotate(
        files=Count('additionalfile__order', filter=Q(additionalfile__deleted=False)),
    )
    result = []
    order_prev = 0
    for order in order_list:
        maket_groups = list(MaketGroup.objects.filter(
            maket__id=order['maket__id'],
            show=True
        ).order_by(
            'name'
        ).values(
            'id',
            'name',
        ))
        for group in maket_groups:
            film_list = Film.objects.filter(groupinfilm__group__id=group['id'], deleted=False).order_by('-date')
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
                'film_number',
                'dateCreate',
                'dateSent',
                'status',
                'groupinfilm__id',
            ))
            group['films'] = film_list_out
        if order['id'] != order_prev:
            order_prev = order['id']
            new_order = {
                'id': order['id'],
                'maketStatus': order['maket_status'],
                'orderNumber': order['order_number'],
                'orderDate': order['order_date'].strftime('%d.%m.%y'),
                'customerName': order['customer__name'],
                'files': order['files'],
                'maketList': [
                    {
                        'id': order['maket__id'],
                        'maketNumber': order['maket__maket_number'],
                        'dateCreate': order['maket__date_create'].strftime('%d.%m.%y'),
                        'comment': order['maket__comment'],
                        'file': order['maket__file'],
                        'maketDeleted': order['maket__deleted'],
                        'groups': maket_groups
                    }
                ]
            }
            result.append(new_order)
        else:
            new_order['maketList'].append(
                {
                    'id': order['maket__id'],
                    'maketNumber': order['maket__maket_number'],
                    'dateCreate': order['maket__date_create'].strftime('%d.%m.%y'),
                    'comment': order['maket__comment'],
                    'file': order['maket__file'],
                    'maketDeleted': order['maket__deleted'],
                    'groups': maket_groups
                }
            )
        new_order['maketQuantity'] = len(list(filter(lambda x: x['file'], new_order['maketList'])))
    return JsonResponse(result, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_file_save(request, maket_id):
    """
    Save maket file to maket table
    :param request:
    :param maket_id:
    :return:maket_file_save/<int:maket_id>
    """
    maket = Maket.objects.get(id=maket_id)
    file_name = ('Макет_' + maket.order.customer.name.replace('"', '').replace(' ', '_')
                 + '_' + maket.order.order_number + '_' + str(maket.maket_number) + '.pdf')

    with open('maket5_0/files/tmp_file', 'rb') as f:
        try:
            os.remove('maket5_0/files/maket/' + file_name)
        except:
            pass
        maket.file.save(file_name, File(f), save=True)
    if maket.file:
        maket.uploaded = True
        maket.save()
        maket.order.maket_status = 'R'
        maket.order.save()
    return JsonResponse(file_name, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_delete(request, maket_id):
    """
    Delete maket file from maket table
    :param request: maket_delete/<int:maket_id>
    :param maket_id:
    :return:
    """
    maket = Maket.objects.get(id=maket_id)
    maket.deleted = True
    maket.save()
    return JsonResponse(maket_id, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_restore(request, maket_id):
    """
    Delete maket file from maket table
    :param request: maket_restore/<int:maket_id>
    :param maket_id:
    :return:
    """
    maket = Maket.objects.get(id=maket_id)
    maket.deleted = False
    maket.save()
    return JsonResponse(maket_id, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_show(request, maket_id):
    maket = Maket.objects.get(id=maket_id)
    try:
        return FileResponse(open(maket.file.path, 'rb'), content_type='application/pdf')
    except:
        return None
