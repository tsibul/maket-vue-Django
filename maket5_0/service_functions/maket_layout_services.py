from django.db.models import Func, F, Value, CharField

from maket5_0.models import OrderPrint, PrintColor, Good, DetailImage, PrintPlaceToPrintPosition, Maket, MaketGroup, \
    OrderItem, MaketPrint
from maket5_0.service_functions import check_printable


def maket_header_info(order):
    """
    Prepare data for maket header
    :param order:
    :return: header_info
    """
    return {
        'number': order.order_number,
        'date': order.order_date.strftime('%d.%m.%y'),
        'supplier': order.supplier,
        'customer': order.customer.name,
    }


def maket_footer_info(order):
    """ Prepare data for maket footer
    :param order: order object
    :return: footer_info
    """
    manager = ''
    manager_info = ''
    if order.manager:
        manager = order.manager.name
        manager_info = order.manager.phone + ' ' + order.manager.mail
    return {
        'supplier': order.supplier,
        'customer': order.customer.name,
        'our_manager': order.our_manager,
        'our_manager_info': 'info@proecopen.ru, office@vikivostok.ru, +7(495)6404825',
        'cst_manager': manager,
        'cst_manager_info': manager_info,
    }


def maket_order_items(order_items, maket_id):
    """
    Prepare data for maket order items
    :param order_items:
    :return: table_contents, item_groups
    """
    item_groups = {}
    i = 0
    for order_item in order_items:
        i = i + 1
        print_items = maket_print_items(order_item, maket_id)
        good_id, good_article = maket_item_goods_data(order_item)
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
    return item_groups


def maket_print_items(order_item, maket_id):
    """
    Prepare print items data for maket print
    :param order_item:
    :return: print_items
    """
    order_prints = OrderPrint.objects.filter(
        item=order_item
    )
    print_items = []
    for print_item in order_prints:
        print_colors = list(PrintColor.objects.filter(
            print_item=print_item
        ).values(
            'id',
            'pantone',
        ))
        image_id, image_list = maket_image_manage(print_item, order_item)
        print_position, print_position_id = maket_print_positions_data(print_item)
        printable = check_printable(print_item)
        maket_print = MaketPrint.objects.filter(maket__id=maket_id, print_item=print_item).first()
        if maket_print:
            checked = maket_print.checked
        else:
            checked = False
        print_items.append({
            'id': print_item.id,
            'place': print_item.place,
            'type': print_item.type,
            'color_quantity': print_item.colors,
            'second_pass': print_item.second_pass,
            'position': print_position,
            'position_id': print_position_id,
            'color': print_colors,
            'printable': printable,
            'image_id': image_id,
            'image_list': image_list,
            'checked': checked,
        })
    return print_items


def maket_item_goods_data(order_item):
    """
    Prepare goods data for order item
    :param order_item:
    :return: good_id, good_article
    """
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
    return good_id, good_article


def maket_show_groups_data(maket_id, item_groups_sorted):
    """
    Prepare show groups data
    :param maket_id:
    :param item_groups_sorted:
    :return: show_groups
    """
    show_groups = None
    if maket_id == 0:
        show_groups = {}
        for key in item_groups_sorted.keys():
            show_groups[key] = True
    return show_groups


def maket_group_patterns_images(item_groups_sorted):
    """
    Prepare patterns & image groups data
    :param item_groups_sorted:
    :return: group_patterns, group_images
    """
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
                    group_images[key].append([
                        detail_image.image_number,
                        f.read(),
                        detail_image.print_position.id,
                        detail_image.print_position.name,
                        detail_image.image_width
                    ])
    return group_patterns, group_images


def maket_image_manage(print_item, order_item):
    """
    Prepare images and image_id
    :param print_item:
    :param order_item:
    :return: print_position, print_position_id
    """
    print_positions_list = PrintPlaceToPrintPosition.objects.filter(
        print_place=print_item.print_place
    ).values_list(
        'print_position__id',
        flat=True
    )
    print_positions = DetailImage.objects.filter(
        goods_image_set__good=order_item.item,
        print_position__id__in=print_positions_list
    )
    image_id = ''
    image_list = []
    if print_positions.count() == 1:
        if not print_item.print_position:
            print_item.print_position = print_positions.first().print_position
            print_item.save()
        image = DetailImage.objects.filter(
            goods_image_set__good=order_item.item,
            print_position=print_item.print_position
        ).first()
        if image:
            image_id = image.image_number
            image_list = [image_id]
    elif print_positions.count() > 1:
        if not print_item.print_position:
            images = DetailImage.objects.filter(
                goods_image_set__good=order_item.item
            )
        else:
            images = DetailImage.objects.filter(
                goods_image_set__good=order_item.item,
                print_position=print_item.print_position
            )
        if images:
            image_list = list(images.values_list('image_number', flat=True))
            image_id = image_list[0]
    return image_id, image_list


def maket_print_positions_data(print_item):
    print_position = ''
    print_position_id = ''
    if print_item.print_position:
        print_position = print_item.print_position.name
        print_position_id = print_item.print_position.id
    return print_position, print_position_id


def sort_by_article(arr):
    """
    Sort item groups by item article
    :param arr (item_groups)
    :return: item_groups sorted by item article
    """
    return sorted(arr, key=lambda x: x['article'])


def maket_tech_info(maket_id, order_id):
    """
    Prepare Maket technical info for layout
    :param order_id:
    :param maket_id:
    :return: tech_info, before_footer
    """
    maket_list = list(
        Maket.objects.filter(
            order__id=order_id
        ).annotate(
            date=Func(
                F('date_create'),
                Value('DD.MM.YYYY'),
                function='TO_CHAR',
                output_field=CharField()
            )
        ).values(
            'id',
            'comment',
            'maket_number',
            'date'
        )
    )
    maket = Maket.objects.filter(id=maket_id).first()
    if maket:
        tech_info = {
            'formatSelected': maket.format_selected,
            'tableShow': maket.table_show,
            'pictureShow': maket.picture_show,
            'frameShow': maket.frame_show,
            'maketId': maket.id,
            'maketDate': maket.date_create.strftime('%d.%m.%Y'),
            'maketNumber': maket.maket_number,
            'maketComment': maket.comment,
            'maketData': maket_list,
            # 'beforeFooter': maket.before_footer
        }
        before_footer = maket.before_footer
    else:
        tech_info = {
            'formatSelected': 1,
            'tableShow': True,
            'pictureShow': False,
            'frameShow': True,
            'maketId': 0,
            'maketNumber': None,
            'maketComment': '',
            'maketData': maket_list,
            # 'beforeFooter': 5
        }
        before_footer = 0
    return tech_info, before_footer


def group_layout_data(maket_id, order_id):
    groups = MaketGroup.objects.filter(maket__id=maket_id)
    group_layout = {}
    if groups.count() > 0:
        for group in groups:
            group_layout[group.name] = {
                'show': group.show,
                'selectAll': group.select_all,
                'spacesBefore': group.spaces_before,
                'showMiniature': group.show_miniature,
            }

    else:
        groups = OrderItem.objects.filter(order__id=order_id).values_list('item_group', flat=True).distinct()
        for group in groups:
            group_layout[group] = {
                'show': True,
                'selectAll': False,
                'spacesBefore': 0,
                'showMiniature': True
            }
    return group_layout
