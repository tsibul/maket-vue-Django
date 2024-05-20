from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Maket, Order, OrderItem, Good, Color
from maket5_0.service_functions import maket_header_info, maket_footer_info, maket_order_items, \
    sort_by_article, maket_show_groups_data, maket_group_patterns_images


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
        'maket': maket_values,
        'itemGroups': item_groups_sorted,
        'showGroups': show_groups,
        'groupPatterns': group_patterns,
        'groupImages': group_images,
        # 'techInfo': None
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


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_save(request):
    return JsonResponse({'id': 'success'}, safe=False)

