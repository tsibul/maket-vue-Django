from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Maket, Order, OrderItem, OrderPrint, PrintColor, PrintType, Good, DetailImage, Color
from maket5_0.service_functions import check_printable


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
        for print_item in order_prints:
            print_colors = '/'.join(PrintColor.objects.filter(print_item=print_item).values_list('pantone', flat=True))
            print_position = ''
            if print_item.print_position:
                print_position = print_item.print_position.name
            printable = check_printable(print_item)
            print_items.append({
                'id': print_item.id,
                'place': print_item.place,
                'type': print_item.type,
                'color_quantity': print_item.colors,
                'second_pass': print_item.second_pass,
                'position': print_position,
                'color': print_colors,
                'printable': printable
            })
        good_id = 0
        good_article = order_item.code.split('.')[0]
        if order_item.item:
            good_id = order_item.item.id
        else:
            goods_obj = Good.objects.filter(article=good_article).first()
            if goods_obj:
                order_item.item = goods_obj
                order_item.save()
                good_id = goods_obj.id
        print_name = order_item.print_name
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
        if order_item.item_group:
            item_key = order_item.item_group
        else:
            item_key = good_article + '()' + print_name
            order_item.item_group = item_key
            order_item.save()
        if item_key not in item_groups:
            item_groups[item_key] = []
        item_groups[item_key].append(table_item)
        table_item['itemGroup'] = item_key
        table_item['inMaket'] = True
        table_contents.append(table_item)

    item_groups_sorted = {k: sort_by_article(v) for k, v in item_groups.items()}
    show_groups = None
    if maket_id == 0:
        show_groups = {}
        for key in item_groups_sorted.keys():
            show_groups[key] = True
    group_patterns = {}
    group_images = {}
    for key in item_groups_sorted.keys():
        goods_article = key.split('()')[0]
        try:
            pattern_name = Good.objects.get(article=goods_article).maket_pattern.name
        except:
            pattern_name = None
        group_patterns[key] = pattern_name
        if Good.objects.filter(article=goods_article).first():
            image_set = DetailImage.objects.filter(goods_image_set__good__article=goods_article)
            group_images[key] = []
            for detail_image in image_set:
                with open(detail_image.svg_file.path, 'r') as f:
                    group_images[key].append([detail_image.image_number, f.read()])

    result = {
        'headerInfo': header_info,
        'footerInfo': footer_info,
        'tableContent': table_contents,
        'maket': maket_values,
        'itemGroups': item_groups_sorted,
        'showGroups': show_groups,
        'groupPatterns': group_patterns,
        'groupImages': group_images
    }
    return JsonResponse(result, safe=False)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_grouping_change(request):
    """
    Change maket grouping
    :param request: maket_grouping_change
    :return:
    """
    for group, item_array in request.data.items():
        if len(item_array):
            filtered_item_array = list(filter(lambda el: el['itemGroup'] != group, item_array))
            for item in filtered_item_array:
                order_item = OrderItem.objects.get(id=item['id'])
                order_item.item_group = group
                order_item.save()
    return JsonResponse({'id': True}, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def item_color_code_list(request, article):
    """
    item_color_code_list returns list of hex colors from article
    :param request: item_color_code_list/<str:article>
    :param article:
    :return: list of hex colors
    """
    color_array = article.split('.')
    good_article = color_array.pop(0)
    color_scheme = Good.objects.filter(article=good_article).first().color_scheme
    hex_array = []
    for color in color_array:
        hex_array.append(Color.objects.filter(color_scheme=color_scheme, code=color).first().hex)
    return JsonResponse({'id': hex_array}, safe=False)


def sort_by_article(arr):
    return sorted(arr, key=lambda x: x['article'])
