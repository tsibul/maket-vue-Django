from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def show_orders(request, order, id_no, search_string, sh_deleted):
    return JsonResponse({})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def import_order(request):
    return JsonResponse({})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_order(request, order_no):
    return JsonResponse({})
