from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Maket


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
