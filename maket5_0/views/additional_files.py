from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Order


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def additional_files_list(request, order_pk):
    order = Order.objects.get(id=order_pk)
    order_number = order.order_number
    return JsonResponse({})
