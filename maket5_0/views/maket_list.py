from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Maket, Order


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def maket_list_info(request, id_no):
    maket_list = Order.objects.filter(
        deleted=False,
        maket__isnull=False
    ).order_by(
        '-order-date',
        '-order_number'
    )[id_no: id_no + 20]

    return JsonResponse(maket_list, safe=False)
