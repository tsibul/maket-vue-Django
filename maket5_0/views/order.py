import datetime
import os

from bs4 import BeautifulSoup
from django.core.files.storage import default_storage
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Customer, Order, Manager
from maket5_0.views import parse_order_html, old_order_delete, update_customer_manager, calculate_prices, \
    order_item_import


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def show_orders(request, order, id_no, search_string, sh_deleted):
    return JsonResponse({})


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
    return JsonResponse({})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_order(request, order_no):
    return JsonResponse({})
