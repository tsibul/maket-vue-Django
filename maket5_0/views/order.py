from django.db.models import Count, Q, Min
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Order, OrderItem, OrderPrint, Maket, MaketGroup, GroupInFilm
from maket5_0.views import parse_order_html, old_order_delete, update_customer_manager, calculate_prices, \
    order_item_import
from maket5_0.views.search_filters import order_search_filter


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def show_orders(request, order, id_no, search_string, sh_deleted):
    id_no = int(id_no)
    if sh_deleted:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(deleted=False)
    if search_string != 'default':
        orders = order_search_filter(orders, search_string)
    if order != 'default':
        orders = orders.order_by(order)
    else:
        orders = orders.order_by(*Order.order_default())
    orders = orders[id_no: id_no + 20]
    orders_out = orders.values(
        'pk',
        'to_check',
        'maket_status',
        'order_number',
        'our_company__code',
        'customer__name',
        'manager__name',
        'manager__mail',
        'manager__phone',
        'order_date',
        'deleted',
    ).annotate(
        maketQuantity=Count('maket__order',
                            filter=Q(maket__deleted=False) & Q(maket__file__isnull=False) & ~Q(maket__file='')),
        files=Count('additionalfile__order', filter=Q(additionalfile__deleted=False)),
        maketId=Min('maket__id', filter=Q(maket__deleted=False)),
    )
    order_list = list(orders_out)
    for order in order_list:
        order['items'] = item_list_for_order(order['pk'])
    return JsonResponse(list(orders_out), safe=False)


# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def item_list(request, pk):
#     items = OrderItem.objects.filter(order__id=pk)
#     json_data = []
#     for item in items:
#         prints = list(
#             OrderPrint.objects.filter(item=item).values('type', 'print_place__name', 'colors', 'second_pass',
#                                                         'print_price'))
#         items_out = {
#             'print_no': item.print_no,
#             'code': item.code,
#             'name': item.name,
#             'print_name': item.print_name,
#             'item_price': item.item_price,
#             'quantity': item.quantity,
#             'prints': prints
#         }
#         json_data.append(items_out)
#     return JsonResponse(json_data, safe=False)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def import_order(request):
    tr_strings = parse_order_html()
    imported_order = Order(user=request.user)
    imported_order.order_from_parse(tr_strings)
    imported_order.update_customer_for_import_order()
    old_order_delete(imported_order)
    cust_manager = update_customer_manager(tr_strings, imported_order.customer)
    imported_order.manager = cust_manager
    imported_order.save()
    order_item_import(tr_strings, imported_order)
    calculate_prices(imported_order)
    order_out = {
        'pk': imported_order.id,
        'to_check': imported_order.to_check,
        'maket_status': imported_order.maket_status,
        'order_number': imported_order.order_number,
        'our_company__code': imported_order.our_company.code,
        'customer__name': imported_order.customer.name,
        'manager__name': imported_order.manager.name,
        'manager__mail': imported_order.manager.mail,
        'order_date': imported_order.order_date,
    }
    order_out['items'] = item_list_for_order(imported_order.id)
    return JsonResponse(order_out, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_order(request, order_no):
    order = Order.objects.get(pk=order_no)
    order.deleted = True
    order.save()
    return JsonResponse({'id': order.id})


def item_list_for_order(pk):
    items = OrderItem.objects.filter(order__id=pk)
    json_data = []
    for item in items:
        prints = list(
            OrderPrint.objects.filter(item=item).values(
                'type',
                'print_place__name',
                'colors',
                'second_pass',
                'print_type__printable',
                'print_price'))
        items_out = {
            'id': item.id,
            'print_no': item.print_no,
            'code': item.code,
            'name': item.name,
            'print_name': item.print_name,
            'item_price': item.item_price,
            'quantity': item.quantity,
            'prints': prints,
            'printsId': item.id,
        }
        json_data.append(items_out)
    return json_data


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def fix_order_errors(request):
    """
    change connection between OrderItems & PrintItems
    :param request: fix_order_errors
    :return:
    """
    result = False
    changed_items = request.data
    new_changed_items = {}
    for item_key in changed_items.keys():
        if int(item_key) != changed_items[item_key]:
            result = True
            new_changed_items[item_key] = list(OrderPrint.objects.filter(item__id=changed_items[item_key]))
    for item_key in new_changed_items.keys():
        for print_item in new_changed_items[item_key]:
            item = OrderItem.objects.get(id=item_key)
            print_item.item = item
            print_item.save()
    if result:
        order = Order.objects.get(orderitem__id=int(list(changed_items.keys())[0]))
        order.to_check = False
        order.save()

    return JsonResponse({'id': result}, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reset_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.maket_status = 'N'
    maket_list = Maket.objects.filter(order=order)
    maket_group_list = MaketGroup.objects.filter(maket__in=maket_list)
    group_in_film_list = GroupInFilm.objects.filter(group__in=maket_group_list)
    for group in group_in_film_list:
        group.delete()
    for maket_group in maket_group_list:
        maket_group.delete()
    for maket in maket_list:
        maket.delete()
    order.save()
    return JsonResponse({'id': order.id})
