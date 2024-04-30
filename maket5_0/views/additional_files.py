from django.db.models import Q
from django.http import JsonResponse, FileResponse, HttpResponse
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Order, AdditionalFile


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def additional_files_list(request, order_pk):
    """
    Create list of additional files and Layouts connected to the specified order
    :param request: additional_file/<int:order_pk>
    :param order_pk: order id
    :return: Dictionary of arrays where key is type of additional file and value is list of additional files as
    dictionary of it's fields
    """
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
    """
    Import additional file  and connect it to order
    :param request: import_additional_file/<int:order_pk>
    :param order_pk: order id to which file be connected
    :return: additional file fields
    """
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
        'order__id': new_file.order.id
    }
    return JsonResponse(result, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def additional_file_show(request, file_pk, file_name):
    """
    Show an additional file if it pdf, and download it in other cases
    :param request: additional_file_show/<int:file_pk>/<str:file_name>
    :param file_pk: additional file id
    :param file_name: additional file name
    :return: file with file name
    """
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
    """
    Delete additional file from order
    :param request: delete_additional_file/<int:file_no>
    :param file_no: file id
    :return: deleted file id
    """
    file = AdditionalFile.objects.get(pk=file_no)
    file.deleted = True
    file.save()
    return JsonResponse({'id': file.id}, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reconnect_additional_file(request, file_no, order_pk):
    """
    Reconnect additional file to new order
    :param request: reconnect_additional_file/<int:file_no>/<int:order_pk>
    :param file_no: file id
    :param order_pk: new order id
    :return: file id, new order id
    """
    file = AdditionalFile.objects.get(pk=file_no)
    order = Order.objects.get(pk=order_pk)
    file.order = order
    file.save()
    return JsonResponse({'fileId': file.id, 'orderId': file.order.id}, safe=False)
