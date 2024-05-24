from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Maket, Order


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_list_info(request, search_string, sh_deleted, id_no):
    order_list = Order.objects.filter(
        maket__isnull=False
    )
    if not sh_deleted:
        order_list = Order.objects.filter(deleted=False)
    if search_string != 'default':
        pass
    order_list = order_list.order_by('-order_date', '-order_number')[id_no: id_no + 20]

    return JsonResponse({'orderList': order_list}, safe=False)
