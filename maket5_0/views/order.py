from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Order, OrderItem, OrderPrint
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
        'deleted'
    ).annotate(
        # maket=Count('maket'),
        files=Count('additionalfile__order', filter=Q(additionalfile__deleted=False))
    )
    return JsonResponse(list(orders_out), safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def item_list(request, pk):
    items = OrderItem.objects.filter(order__id=pk)
    json_data = []
    for item in items:
        prints = list(
            OrderPrint.objects.filter(item=item).values('type', 'print_place__name', 'colors', 'second_pass',
                                                        'print_price'))
        items_out = {
            'print_no': item.print_no,
            'code': item.code,
            'name': item.name,
            'print_name': item.print_name,
            'item_price': item.item_price,
            'quantity': item.quantity,
            'prints': prints
        }
        json_data.append(items_out)
    return JsonResponse(json_data, safe=False)


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
    order_out={
        'pk': imported_order.id,
        'to_check': imported_order.to_check,
        'maket_status': imported_order.maket_status,
        'order_number': imported_order.order_number,
        'our_company__code': imported_order.our_company.code,
        'customer__name': imported_order.customer.name,
        'manager__name': imported_order.manager.name,
        'manager__mail': imported_order.manager.mail,
        'order_date': imported_order.order_date
    }
    return JsonResponse(order_out, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_order(request, order_no):
    order = Order.objects.get(pk=order_no)
    order.deleted = True
    order.save()
    return JsonResponse({'id': order.id})
