from django.http import JsonResponse
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import PantoneToHex


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def hex_from_pantone(request, pantone):
    """
    Receive hex from pantone
    :param request: 'hex_from_pantone/<str:pantone>'
    :param pantone:
    :return: hex_color
    """
    hex_color = '#FFFFFF'
    hex_obj = PantoneToHex.objects.filter(name=pantone).first()
    if hex_obj:
        hex_color = hex_obj.hex
    return JsonResponse({'hex': hex_color}, safe=False)


