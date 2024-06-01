from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Film


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def film_list_for_group(request, group_id, connected):
    """

    :param request: film_list_for_group/<int:group_id>/<int:connected>
    :param group_id:
    :param connected:
    :return:
    """
    if connected:
        film_list = Film.objects.filter(groupinfilm__group__id=group_id, deleted=False).order_by('-date')
    else:
        film_list = Film.objects.filter(~Q(groupinfilm__group__id=group_id) & Q(deleted=False)).order_by('-date')
    film_list = Film.objects.filter(groupinfilm__group__id=group_id, deleted=False).order_by('-date')
    film_list_out = film_list.values(
        'film_number',
        'date',
        'date_sent'
        'status'
        'groupinfilm__id'
    )
    return JsonResponse(film_list_out, safe=False)
