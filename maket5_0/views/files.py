import os

from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import AdditionalFile, Pattern


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def files_additional_file(request, search_string, id_no, sh_undeleted):
    files = AdditionalFile.objects.all()
    if sh_undeleted == 0:
        files = files.filter(Q(deleted=True) | Q(order__deleted=True)).distinct()
    if search_string != 'default':
        files = files.filter(
            name__icontains=search_string,
            additional_file_name__icontains=search_string,
            order__order_number__icontains=search_string,
            order__order__customer_name__icontains=search_string
        )
    files = files[id_no: id_no + 20]
    result = files.values(
        'id',
        'name',
        'additional_file_name',
        'order__order_number',
        'order__customer_name',
    )
    return JsonResponse(list(result), safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def files_additional_file_delete(request, file_id):
    file_obj = AdditionalFile.objects.get(id=file_id)
    file = file_obj.additional_file
    answer = {'id': 0}
    if delete_file_from_disk(file, file_obj):
        answer['id'] = file_id
    return JsonResponse(answer, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def files_additional_file_delete_all(request):
    files = AdditionalFile.objects.filter(Q(deleted=True) | Q(order__deleted=True)).distinct()
    answer = delete_all(files)
    return JsonResponse(answer, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def files_pattern(request, search_string, id_no, sh_undeleted):
    files = Pattern.objects.all()
    if sh_undeleted == 0:
        files = files.filter(deleted=True)
    if search_string != 'default':
        files = files.filter(
            name__icontains=search_string,
            good__name__icontains=search_string,
            good__article__icontains=search_string,
        )
    files = files[id_no: id_no + 20]
    result = files.values(
        'id',
        'name',
        'file',
        'good__article',
        'good__name'
    )
    return JsonResponse(list(result), safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def files_pattern_delete(request, file_id):
    file_obj = Pattern.objects.get(id=file_id)
    file = file_obj.file
    answer = {'id': 0}
    if delete_file_from_disk(file, file_obj):
        answer['id'] = file_id
    return JsonResponse(answer, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def files_pattern_delete_all(request):
    files = Pattern.objects.filter(deleted=True)
    answer = delete_all(files)
    return JsonResponse(answer, safe=False)


def delete_file_from_disk(file, file_obj):
    file_path = file.path
    try:
        os.remove(file_path)
        file_obj.delete()
        return True
    except:
        return False


def delete_all(files):
    answer = {'deleted': True}
    for file_obj in files:
        file = file_obj.file
        if not delete_file_from_disk(file, file_obj):
            answer = {'deleted': True}
    return answer
