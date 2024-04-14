from bs4 import BeautifulSoup

from maket5_0.models import Order, Manager


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
    if customer_manager_mail != '' and customer_manager_mail != '\xa0':
        imp_managers = Manager.objects.filter(manager_mail=customer_manager_mail, deleted=False)
        for imp_manager in imp_managers:
            if imp_manager.name == customer_manager_name:
                cust_manager = imp_manager
                break
        else:
            cust_manager = Manager(name=customer_manager_name, phone=customer_manager_phone,
                                   mail=customer_manager_mail, customer_group=customer.customer_group)
            cust_manager.save()
    else:
        cust_manager = Manager(name=customer_manager_name, phone=customer_manager_phone,
                               customer_group=customer.customer_group)
        cust_manager.save()
    return cust_manager
