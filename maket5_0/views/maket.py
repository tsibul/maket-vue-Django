from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Maket, Order, OrderItem, OrderPrint, PrintColor


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
    manager = ''
    manager_info = ''
    if order.manager:
        manager = order.manager.name
        manager_info = order.manager.phone + ' ' + order.manager.mail
    footer_info = {
        'supplier': order.supplier,
        'customer': order.customer.name,
        'our_manager': order.our_manager,
        'our_manager_info': 'info@proecopen.ru, office@vikivostok.ru, +7(495)6404825',
        'cst_manager': manager,
        'cst_manager_info': manager_info,
    }
    order_items = OrderItem.objects.filter(order__id=order_id).order_by('item__article')
    table_contents = []
    item_groups = {}
    i = 0
    for order_item in order_items:
        i = i + 1
        order_prints = OrderPrint.objects.filter(item=order_item)
        print_items = []
        for print in order_prints:
            print_colors = '/'.join(PrintColor.objects.filter(print_item=print).values_list('pantone', flat=True))
            print_position = ''
            if print.print_position:
                print_position = print.print_position.name
            print_items.append({
                'id': print.id,
                'place': print.place,
                'type': print.type,
                'color_quantity': print.colors,
                'second_pass': print.second_pass,
                'position': print_position,
                'color': print_colors
            })
        good_id = 0
        if order_item.item:
            good_id = order_item.item.id
        print_name = order_item.print_name
        good_article = order_item.code.split('.')[0]
        table_item = {
            'id': order_item.id,
            'no': i,
            'good_id': good_id,
            'article': order_item.code,
            'good_article': good_article,
            'name': order_item.name,
            'print_name': print_name,
            'quantity': order_item.quantity,
            'print_item': print_items,
        }
        item_key = good_article + '()' + print_name
        if item_key not in item_groups:
            item_groups[item_key] = []
        item_groups[item_key].append(table_item)
        table_item['itemGroup'] = item_key
        table_item['inMaket'] = True
        table_contents.append(table_item)
    result = {
        'headerInfo': header_info,
        'footerInfo': footer_info,
        'tableContent': table_contents,
        'maket': maket_values,
        'itemGroups': item_groups,
    }
    return JsonResponse(result, safe=False)