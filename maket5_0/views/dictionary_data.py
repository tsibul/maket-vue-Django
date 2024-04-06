import json
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from maket5_0 import models
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.service_functions import linking_filter


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dictionary_records(request, dict_type, id_no, order, search_string, sh_deleted):
    dict_items = dict_additional_filter(dict_type, order, id_no, search_string, sh_deleted)
    # formatted_dict_items = [format_datetime_fields(item) for item in dict_items]
    return JsonResponse(list(dict_items), safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dictionary_filter(request, dict_type, filter_dictionary, filter_dictionary_id):
    """
    Using for table connection if we find item in second table in second table
    filter parent table by it
    :param request:
    :param dict_type:
    :param filter_dictionary:
    :param filter_dictionary_id:
    :return:
    """
    if dict_type == 'default':
        formatted_dict_items = []
        json_dict = json.dumps(formatted_dict_items, ensure_ascii=False, default=str)
        return JsonResponse(json_dict, safe=False)
    dict_model = getattr(models, dict_type)
    if filter_dictionary != 'default':
        filter_model = getattr(models, filter_dictionary)
        filter_item = linking_filter(dict_model, filter_model, filter_dictionary_id)
    else:
        filter_item = dict_model.objects.filter(deleted=False)
        if dict_type == 'CustomerGroup':
            filter_item = filter_item.filter(default=False)
    choices_field = None
    for field in dict_model.dictionary_fields():
        try:
            field['emitChoices']
            choices_field = field['field']
        except:
            pass
    if choices_field:
        formatted_dict_items = [{item.id: str(item), 'choices': getattr(item, choices_field)} for item in filter_item]
    else:
        formatted_dict_items = [{item.id: str(item)} for item in filter_item]
    return JsonResponse(formatted_dict_items, safe=False)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dictionary_update(request, dict_type):
    dict_id = request.data['id']
    dict_model = getattr(models, dict_type)
    field_list = dict_model.dictionary_fields()
    if dict_id != '0':
        dict_element = dict_model.objects.get(id=dict_id)
    else:
        dict_element = dict_model()
    for field in field_list:
        request_data = request.data[field['field']]
        if field['type'] == 'string':
            setattr(dict_element, field['field'], request_data)
        elif field['type'] == 'boolean':
            setattr(dict_element, field['field'], request_data)
        elif field['type'] == 'foreign':
            foreign_model = getattr(models, field['foreignClass'])
            foreign_element = foreign_model.objects.get(id=request_data)
            setattr(dict_element, field['field'], foreign_element)
    dict_element.save()
    return JsonResponse({'id': dict_element.id})


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dictionary_delete(request, dict_type, record_id):
    """

    :param request:
    :param dict_type:
    :param record_id:
    :return:
    """
    dict_model = getattr(models, dict_type)
    record = dict_model.objects.get(id=record_id)
    record.deleted = True
    return JsonResponse({'id': record.id})


def dict_additional_filter(dict_type, order, id_no, search_string, sh_deleted):
    dict_model = getattr(models, dict_type)
    order_calculated = dict_model.order_default()
    if order != 'default':
        order_calculated = order
    dict_items = dict_model.objects.all().order_by(*order_calculated)
    if sh_deleted == 0:
        dict_items = dict_items.filter(deleted=False)
    if search_string == 'default':
        if dict_type == 'CustomerGroup':
            dict_items = dict_items.filter(default=False)
    if search_string != 'default':
        search_string = search_string.replace('_', ' ')
        filter_items = dict_items
        dict_items = filter_items.filter(id=0)
        for field in dict_model.dictionary_fields():
            if field['type'] == 'string':
                field_name = field['field'] + '__icontains'
                dict_items = dict_items | filter_items.filter(**{field_name: search_string})
            elif field['type'] == 'foreign':
                foreign_model = getattr(models, field['foreignClass'])
                for key in foreign_model.dictionary_fields():
                    if key['type'] == 'text':
                        field_name = field['field'] + '__' + key['field'] + '__icontains'
                        dict_items = dict_items | filter_items.filter(**{field_name: search_string})
    dict_items = dict_items.distinct()[id_no: id_no + 20]
    output = []
    for item in dict_items:
        current_dict = {'id': item.id, 'fields': []}
        for field in dict_model.dictionary_fields():
            if field['type'] == 'boolean':
                result = 'да' if getattr(item, field['field']) else 'нет'
                current_dict['fields'].append(result)
            elif field['type'] != 'foreign':
                current_dict['fields'].append(getattr(item, field['field']))
            else:
                current_dict['fields'].append(str(getattr(item, field['field'])))
        output.append(current_dict)
    return output


def format_datetime_fields(item):
    """
    Format date field and return hex color if exists
    :param item:
    :return:
    change datetime param fo js, returns hex color if exists
    """
    formatted_item = {}
    item_dict = item.__dict__
    for field in item_dict.keys():
        if isinstance(item_dict[field], datetime):
            formatted_item[field] = item_dict[field].strftime('%d.%m.%y %H:%M')
        else:
            if field[0:1] != "_":
                formatted_item[field] = item_dict[field]
                if field[-3:] == "_id":
                    if type(getattr(item, field[0:-3])).__name__ == 'User':
                        formatted_item[field[0:-3]] = getattr(getattr(item, field[0:-3]), 'last_name')
                    else:
                        formatted_item[field[0:-3]] = str(getattr(item, field[0:-3]))
    return formatted_item


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dictionary_single_record(request, dict_type, record_id):
    """

    :param request:
    :param dict_type:
    :param record_id:
    :return:
    """
    dict_model = getattr(models, dict_type)
    record = dict_model.objects.get(id=record_id)
    fields = dict_model.dictionary_fields()
    record_data = {}
    for field in fields:
        if field['type'] == 'foreign':
            field_object = getattr(record, field['field'])
            record_data.update({field['field'] + '_id': field_object.id})
            record_data.update({field['field']: field_object.name})
        else:
            record_data.update({field['field']: getattr(record, field['field'])})

    return JsonResponse(record_data, safe=False)
