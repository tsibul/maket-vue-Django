import datetime

from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Maket, Order, OrderItem, Good, Color, MaketGroup, OrderPrint, PrintPosition, MaketPrint, \
    PrintColor
from maket5_0.service_functions import maket_header_info, maket_footer_info, maket_order_items, \
    sort_by_article, maket_show_groups_data, maket_group_patterns_images, maket_tech_info, group_layout_data


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
    order = Order.objects.get(id=order_id)

    tech_info, before_footer = maket_tech_info(maket_id, order_id)
    group_layout = group_layout_data(maket_id, order_id)
    header_info = maket_header_info(order)
    footer_info = maket_footer_info(order)
    order_items = OrderItem.objects.filter(order__id=order_id).order_by('code')
    item_groups = maket_order_items(order_items)
    item_groups_sorted = {k: sort_by_article(v) for k, v in item_groups.items()}
    show_groups = maket_show_groups_data(maket_id, item_groups_sorted)
    group_patterns, group_images = maket_group_patterns_images(item_groups_sorted)
    result = {
        'headerInfo': header_info,
        'footerInfo': footer_info,
        'itemGroups': item_groups_sorted,
        'showGroups': show_groups,
        'groupPatterns': group_patterns,
        'groupImages': group_images,
        'techInfo': tech_info,
        'beforeFooter': before_footer,
        'groupLayoutData': group_layout,
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
    good_object = Good.objects.filter(article=good_article).first()
    article_length = good_object.detail_quantity
    color_scheme = good_object.color_scheme
    hex_array = []
    length_difference = article_length - len(color_array)
    j = 0
    for color in color_array:
        color_last = Color.objects.filter(color_scheme=color_scheme, code=color).first().hex
        hex_array.append(color_last)
        j = j + 1
        if j == -length_difference:
            break
    if length_difference:
        for i in range(length_difference):
            hex_array.append(color_last)
    return JsonResponse({'id': hex_array}, safe=False)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_save(request):
    maket_id = request.data['maket_id']
    order_id = request.data['order_id']
    order = Order.objects.get(id=order_id)
    if int(maket_id):
        maket = Maket.objects.get(id=int(maket_id))
        maket.date_modified = datetime.date.today()
    else:
        maket = Maket(order=order, date_create=datetime.date.today())
    maket.maket_number = request.data['tech_info']['maketNumber']
    if not maket.maket_number:
        maket.maket_number = 1
    maket.format_selected = request.data['tech_info']['formatSelected']
    maket.frame_show = request.data['tech_info']['frameShow']
    maket.comment = request.data['tech_info']['maketComment']
    maket.picture_show = request.data['tech_info']['pictureShow']
    maket.table_show = request.data['tech_info']['tableShow']
    maket.before_footer = request.data['before_footer']
    maket.save()

    group_data = request.data['group_layout']
    # show_groups = request.data['show_groups']
    for group in group_data.keys():
        maket_group = MaketGroup.objects.filter(name=group, maket=maket).first()
        if not maket_group:
            maket_group = MaketGroup(name=group, maket=maket)
        maket_group.show = group_data[group]['show']
        maket_group.show_miniature = group_data[group]['showMiniature']
        maket_group.spaces_before = group_data[group]['spacesBefore']
        maket_group.select_all = group_data[group]['selectAll']
        maket_group.save()
        order.maket_status = 'P'
        order.save()
    item_data = request.data['item_data']
    for group in item_data.values():
        for item in group:
            for prt_item in item['print_item']:
                print_item = OrderPrint.objects.get(id=prt_item['id'])
                print_position = PrintPosition.objects.get(id=prt_item['position_id'])
                print_item.print_position = print_position
                print_item.save()
                maket_print = MaketPrint.objects.filter(print_item=print_item, maket=maket).first()
                if not maket_print:
                    maket_print = MaketPrint(print_item=print_item, maket=maket)
                try:
                    print_checked = prt_item['checked']
                    maket_print.checked = print_checked
                except:
                    maket_print.checked = False
                maket_print.save()
                for color in prt_item['color']:
                    print_color = PrintColor.objects.get(id=color['id'])
                    print_color.pantone = color['pantone']
                    print_color.save()
    return JsonResponse({'id': maket.id}, safe=False)
