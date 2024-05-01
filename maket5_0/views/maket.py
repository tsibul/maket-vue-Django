from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Maket, Order, OrderItem, OrderPrint


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_to_order(request, order_no):
    """
    Return list of maket objects for given order
    :param request:maket_to_order/<int:order_no>
    :param order_no: order.id
    :return:
    """
    maket_list = list(Maket.objects.filter(
        order__id=order_no
    ).values(
        'id',
        'maket_number',
        'comment'
    ))
    return JsonResponse(maket_list, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_info(request, maket_id, order_id):
    """
    Return maket info for given maket_id & order_id
    :param order_id:
    :param maket_id:
    :param request:maket_info/<int:maket_id>/<int:order_id>
    :return:
    """
    maket = Maket.objects.filter(id=maket_id)
    maket_values = ''
    if maket:
        maket_values = maket.values()
    order = Order.objects.get(id=order_id)
    header_info = {
        'number': order.order_number,
        'date': order.order_date.strftime('%d.%m.%y'),
        'supplier': order.supplier,
        'customer': order.customer.name,
    }
    footer_info = {
        'supplier': order.supplier,
        'customer': order.customer.name,
        'our_manager': order.our_manager,
        'our_manager_info': 'info@proecopen.ru, office@vikivostok.ru, +7(495)6404825',
        'cst_manager': order.manager.name,
        'cst_manager_info': order.manager.phone + ' ' + order.manager.mail,
    }
    order_items = OrderItem.objects.filter(order__id=order_id)
    order_prints = list(OrderPrint.objects.filter(item__in=order_items).values())
    result = {'headerInfo': header_info,
              'footerInfo': footer_info,
              'maket': maket_values,
              'order_prints': list(order_prints),
              'order_items': list(order_items.values())}
    return JsonResponse(result, safe=False)
