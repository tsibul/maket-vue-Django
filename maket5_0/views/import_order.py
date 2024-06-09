from bs4 import BeautifulSoup
from django.db.models import Sum

from maket5_0.models import Order, Manager, Good, OrderItem, OrderPrint, PrintPlace, PrintColor, PrintType


def parse_order_html():
    with open('maket5_0/files/tmp_file', 'r', encoding="utf-8") as tmp:
        # demo = tmp.read()
        soup_html = BeautifulSoup(tmp, "html.parser")
        soup_tr = soup_html.find_all("tr")
        tr_strings = []
        for tr in soup_tr:
            tmp_tr = tr.contents
            tmp_strings = []
            for td in tmp_tr:
                try:
                    tmp_td = td.contents[0]
                    if tmp_td != '':
                        if len(td.contents) > 1:
                            td.select_one('br').decompose()
                            tmp_td = ' '.join(td.contents)
                        tmp_strings.append(tmp_td)
                except:
                    pass
            if tmp_strings:
                tr_strings.append(tmp_strings)
    return tr_strings


def old_order_delete(order):
    old_orders = Order.objects.filter(order_number=order.order_number, deleted=False)
    if old_orders:
        for old_order in old_orders:
            old_order.deleted = True
            old_order.save()


def update_customer_manager(tr_strings, customer):
    customer_manager_name = str(tr_strings[15][0])
    customer_manager_mail = str(tr_strings[16][0])
    customer_manager_phone = str(tr_strings[17][0])
    cust_manager = None
    if customer_manager_mail != '' and customer_manager_mail != '\xa0':
        cust_manager = Manager.objects.filter(name=customer_manager_name, mail=customer_manager_mail, deleted=False).first()
    elif customer_manager_phone != '' and customer_manager_phone != '\xa0':
        cust_manager = Manager.objects.filter(name=customer_manager_name, phone=customer_manager_phone, deleted=False).first()
    elif customer_manager_name != '' and customer_manager_name != '\xa0':
        cust_manager = Manager.objects.filter(name=customer_manager_name, deleted=False).first()
    if not cust_manager and customer_manager_name != '' and customer_manager_name != '\xa0':
        cust_manager = Manager(name=customer_manager_name, phone=customer_manager_phone,
                               mail=customer_manager_mail, customer_group=customer.customer_group)
        cust_manager.save()
    return cust_manager


def order_item_import(tr_strings, order):
    order_body = range(19, len(tr_strings), 1)

    items = {}
    for i in order_body:
        tr_len = len(tr_strings[i])
        if tr_strings[i][tr_len - 1] == '1sec_endofline':
            item = OrderItem(order=order)
            item.item_from_order_import(i, tr_strings)
            item.save()
            if item.name in items.keys():
                items[item.name].append(item)
            else:
                items[item.name] = [item]
        if tr_strings[i][tr_len - 1] == '2 sec_endofline':
            if tr_len == 9:
                if tr_strings[i][0] and tr_strings[i][0] != '\xa0':
                    print_no = tr_strings[i][0]
                    item_name = tr_strings[i][1]
                    item = items[item_name].pop(0)
                    item_price = float(tr_strings[i][2].replace(',', '.'))
                    item.item_price = item_price
                    item.save()
                    if print_no != item.print_no or len(items[item.name]) > 0:
                        order.to_check = True
                        order.save()
                place = tr_strings[i][3]
                try:
                    int(place.split(' ')[-1])
                    place_name = place[0: -2]
                except:
                    place_name = place
                print_place = PrintPlace.objects.filter(name=place_name).first()
                type = tr_strings[i][4]
                print_type = PrintType.objects.filter(name=type).first()
                colors = int(tr_strings[i][5])
                print_price = float(tr_strings[i][7].replace(',', '.'))
                second_pass = tr_strings[i][6] != '-'
                order_print = OrderPrint(
                    place=place,
                    print_place=print_place,
                    type=type,
                    print_type=print_type,
                    colors=colors,
                    second_pass=second_pass,
                    item=item,
                    print_no=print_no,
                    print_price=print_price,
                )
                order_print.save()
                for i in range(colors):
                    print_color = PrintColor(number_in_item=i, print_item=order_print)
                    print_color.save()


def calculate_prices(ord_imp):
    items_for_price = OrderItem.objects.filter(order=ord_imp)
    gross_prt_quantity = 0
    gross_prt_price = 0
    for item in items_for_price:
        prts_for_price = OrderPrint.objects.filter(item=item)
        prt_quantity = len(prts_for_price)
        prt_price = prts_for_price.aggregate(total=Sum('print_price'))['total']
        gross_prt_quantity = gross_prt_quantity + prt_quantity * item.quantity
        if prt_price:
            gross_prt_price = gross_prt_price + prt_price * item.quantity
        item.print_price = prt_price if prt_price else 0
        item.num_prints = prt_quantity
        item.save()
    ord_imp.print_quantity = gross_prt_quantity
    ord_imp.print_sum = gross_prt_price
    ord_imp.save()
