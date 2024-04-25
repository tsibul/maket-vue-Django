from django.db.models import Q
from django.http import JsonResponse, FileResponse, HttpResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Order, AdditionalFile


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def additional_files_list(request, order_pk):
    order = Order.objects.get(id=order_pk)
    order_number = order.order_number
    main_files = AdditionalFile.objects.filter(
        order=order,
        deleted=False,
    ).values(
        'id',
        'name',
        'additional_file_name',
        'file_type',
    )
    deleted_files = AdditionalFile.objects.filter(
        Q(order__order_number=order_number) &
        ~Q(order=order) &
        Q(deleted=False)
    ).values(
        'id',
        'name',
        'additional_file_name',
        'file_type',
        'order__id'
    )
    return JsonResponse({'main': list(main_files), 'deleted': list(deleted_files), 'maket': []}, safe=False)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def import_additional_file(request, order_pk):
    order = Order.objects.get(id=order_pk)
    additional_file = request.data['file']
    additional_file_type = request.data['file_type']
    additional_file_name = additional_file.name
    new_file = AdditionalFile(
        name=additional_file_type,
        additional_file=additional_file,
        additional_file_name=additional_file_name,
        order=order
    )
    new_file.save()
    result = {
        'id': new_file.id,
        'name': new_file.name,
        'additional_file_name': new_file.additional_file.name,
        'file_type': new_file.file_type,
    }
    return JsonResponse(result, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def additional_file_show(request, file_pk, file_name):
    file = AdditionalFile.objects.get(id=file_pk)
    if file.file_type == '.pdf':
        try:
            return FileResponse(open(file.additional_file.path, 'rb'), content_type='application/pdf')
        except:
            return None
    else:
        try:
            return FileResponse(open(file.additional_file.path, 'rb'), content_type='application/force-download')
        except:
            return None


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_additional_file(request, file_no):
    file = AdditionalFile.objects.get(pk=file_no)
    file.deleted = True
    file.save()
    return JsonResponse({'deletedId': file.id})
