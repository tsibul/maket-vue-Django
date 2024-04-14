import datetime
import os

from bs4 import BeautifulSoup
from django.core.files.storage import default_storage
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Customer


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def show_orders(request, order, id_no, search_string, sh_deleted):
    return JsonResponse({})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def import_order(request):
    try:
        os.remove('tmp_file')
    except:
        pass
    file = request.FILES['Chosen']
    default_storage.save('tmp_file', file)
    tmp = open('tmp_file', 'r', encoding="utf-8")
    demo = tmp.read()
    soup_html = BeautifulSoup(demo, "html.parser")
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

    number_tr = len(tr_strings)
    order_no = str(tr_strings[2][0])
    order_date = tr_strings[1][0]
    order_date = datetime.datetime.strptime(order_date, '%d.%m.%Y').date()
    supplier = str(tr_strings[4][0])
    customer_name = str(tr_strings[6][0])
    customer_inn = str(tr_strings[7][0])
    customer_address = str(tr_strings[8][0])
    order_quantity = str(tr_strings[10][0])
    ord_sum = str(tr_strings[12][0])
    order_sum = ord_sum.replace(',', '.')
    our_manager = str(tr_strings[13][0])
    #    our_manager_phone = str(tr_strings[14][0])
    customer_manager = str(tr_strings[15][0])
    customer_manager_phone = str(tr_strings[17][0])
    customer_manager_mail = str(tr_strings[16][0])
    # if customer_manager_mail != '' and customer_manager_mail != '\xa0':
    #     try:
    #         imp_manager = Manger.orders.get(manager_mail=customer_manager_mail)
    #         if imp_manager.manager == customer_manager:
    #             customer_manager = imp_manager
    #         else:
    #             cust_manager = Manger(manager=customer_manager, manager_phone=customer_manager_phone,
    #                                   manager_mail=customer_manager_mail)
    #     except:
    #         cust_manager = Manger(manager=customer_manager, manager_phone=customer_manager_phone,
    #                               manager_mail=customer_manager_mail)
    # else:
    #     cust_manager = Manger(manager=customer_manager, manager_phone=customer_manager_phone)
    # cust_manager.save()
    # try:
    #     ord_imp = Order_imports.objects.get(order_id=order_no)
    #     ord_imp.delete()
    # except:
    #     pass
    # ord_imp = Order_imports(order_id=order_no, supplier=supplier, customer_name=customer_name,
    #                         customer_INN=customer_inn, customer_address=customer_address, order_date=order_date,
    #                         order_quantity=order_quantity, order_sum=order_sum, our_manager=our_manager,
    #                             manager=cust_manager)
    # try:
    #     if len(customer_inn) >= 10:
    #         customer = Customer.objects.get(inn=customer_inn)
    #         ord_imp.customer = customer
    #     elif len(customer_inn) <= 10:
    #         customer = Customer.objects.get(name=customer_name)
    #         ord_imp.customer = customer
    #         typegroup_in = order_no[slice(13, 15)]
    #         if customer.customer_type != typegroup_in:
    #             customer.customer_type = typegroup_in
    #             customer.save()
    # except:
    #     region = customer_inn[slice(0, 2)]
    #     typegroup_in = order_no[slice(13, 15)]
    #     try:
    #         typegroup = Customer_types.objects.get(code=typegroup_in)
    #     except:
    #         typegroup = ''
    #     try:
    #         if len(customer_inn) >= 10:
    #             customer_all = Customer_all.objects.filter(inn=customer_inn).order_by('frigat_id').last()
    #         else:
    #             customer_all = Customer_all.objects.filter(customer_name__in=customer_name).order_by('frigat_id').last()
    #     except:
    #         customer_all = None
    #     customer = Customer(name=customer_name, address=customer_address, inn=customer_inn, region=region,
    #                         customer_type=typegroup, customer_all=customer_all)
    #     if customer_all:
    #         customer_all.customer_type = typegroup
    #         customer_all.save()
    #         customer.frigat_id = customer_all.frigat_id
    #     customer.save()
    #     ord_imp.customer = customer
    # ord_imp.save()
    # order_body = range(19, number_tr, 1)
    # items_list = []
    # print_list = []
    # prnt_list = {}
    # for i in order_body:
    #     tr_len = len(trstrings[i])
    #     if trstrings[i][tr_len - 1] == '1sec_endofline' and trstrings[i][3] != '\xa0':
    #         itm_clr = trstrings[i][2].split('.')
    #         itm_group = itm_clr[0]
    #         prt_name = trstrings[i][3]
    #         try:
    #             itm_obj = Detail_set.objects.get(item_name=itm_group)
    #         except:
    #             pass
    #
    #         if len(prt_name) >= 16:
    #             pr_nm = prt_name[0: 12]
    #         elif 15 > len(prt_name) > 11:
    #             pr_nm = prt_name[0: 7]
    #         else:
    #             pr_nm = prt_name[0: 3]
    #         if itm_obj.print_group not in prnt_list:
    #             prnt_list[itm_obj.print_group] = []
    #         if len(prnt_list[itm_obj.print_group]) == 0:
    #             prnt_list[itm_obj.print_group].append(prt_name)
    #         else:
    #             tmp = False
    #             for pr in prnt_list[itm_obj.print_group]:
    #                 if pr.find(pr_nm) == 0:
    #                     prt_name = pr
    #                     tmp = True
    #             if not tmp:
    #                 prnt_list[itm_obj.print_group].append(prt_name)
    #                 tmp = False
    #         itm_clr.pop(0)
    #         clr = '.'.join(itm_clr)
    #         num_details = len(itm_clr)
    #         x = range(num_details)
    #         item = Item_imports(print_id=trstrings[i][0], code=trstrings[i][2], name=trstrings[i][1],
    #                             quantity=trstrings[i][4], print_name=prt_name, order=ord_imp,
    #                             item_group=itm_group, item_color=clr, item=itm_obj)
    #         for n in x:
    #             detail = 'detail' + str(n + 1) + '_color'
    #             detail_hex = 'detail' + str(n + 1) + '_hex'
    #             setattr(item, detail, itm_clr[n])
    #             try:
    #                 hex_color = Item_color.objects.get(
    #                     Q(color_id=itm_clr[n]) & Q(color_scheme=item.item.color_scheme)).color_code
    #                 setattr(item, detail_hex, hex_color)
    #             except:
    #                 pass
    #         item.save()
    #         items_list.append(item)
    #
    #     elif trstrings[i][tr_len - 1] == '2 sec_endofline':
    #         max_len = 0
    #         for v in prnt_list.values():
    #             if max_len < len(v):
    #                 max_len = len(v)
    #         if max_len == 1:
    #             for x in items_list:
    #                 if x.name == trstrings[i][1]:
    #                     prt_item = x
    #         elif items_list[len(items_list) - 1].print_id == str(len(items_list)):
    #             ord_imp.to_check = True
    #             for x in items_list:
    #                 if x.print_id == trstrings[i][0]:
    #                     prt_item = x
    #         else:
    #             ord_imp.to_check = True
    #             for x in items_list:
    #                 if x.name == trstrings[i][1]:
    #                     prt_item = x
    #         if tr_len == 9:
    #             place = trstrings[i][3]
    #             type = trstrings[i][4]
    #             colors = trstrings[i][5]
    #             itm_price = trstrings[i][2].split(',')
    #             if itm_price != ['\xa0']:
    #                 try:
    #                     item_price = float(itm_price[0]) + int(itm_price[1]) / 10 ** len(itm_price[1])
    #                 except:
    #                     item_price = float(itm_price[0])
    #                 itm_for_price = Item_imports.objects.get(id=prt_item.id)
    #                 itm_for_price.item_price = item_price
    #                 itm_for_price.save()
    #             prt_price = trstrings[i][7].split(',')
    #             try:
    #                 print_price = float(prt_price[0]) + int(prt_price[1]) / 10 ** len(prt_price[1])
    #             except:
    #                 print_price = float(prt_price[0])
    #             if trstrings[i][6] == '-':
    #                 second_pass = False
    #             else:
    #                 second_pass = True
    #         place_obj = place_obj_from_place(place)
    #         print_item = Print_imports(place=place, type=type, colors=colors, item=prt_item, print_id=prt_item.print_id,
    #                                    second_pass=second_pass, print_price=print_price, print_place=place_obj)
    #         print_item.save()
    #         print_pos = print_position_and_color_from_print_obj(place, print_item)
    #         if print_pos != '':
    #             print_item.print_position = print_pos
    #             print_item.save()
    #         print_color_check(print_item)
    #         print_list.append([place, type, colors, second_pass, print_item, print_item.print_id])
    # itms_for_price = Item_imports.objects.filter(order=ord_imp)
    # gross_prt_quantity = 0
    # gross_prt_price = 0
    # for itm in itms_for_price:
    #     prts_for_price = Print_imports.objects.filter(item=itm)
    #     prt_price = 0.0
    #     prt_quantity = len(prts_for_price)
    #     for prt in prts_for_price:
    #         prt_price = prt_price + prt.print_price
    #     gross_prt_quantity = gross_prt_quantity + prt_quantity * itm.quantity
    #     gross_prt_price = gross_prt_price + prt_price * itm.quantity
    #     itm.print_price = prt_price
    #     itm.num_prints = prt_quantity
    #     itm.save()
    # ord_imp.print_quantity = gross_prt_quantity
    # ord_imp.print_sum = gross_prt_price
    # ord_imp.save()
    return JsonResponse({})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_order(request, order_no):
    return JsonResponse({})
