from datetime import datetime

from django.http import JsonResponse
from maket5_0 import models
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dictionary_records(request, dict_type, id_no, order, search_string, sh_deleted):
    dict_items = dict_additional_filter(dict_type, order, id_no, search_string, sh_deleted)
    # formatted_dict_items = [format_datetime_fields(item) for item in dict_items]
    return JsonResponse(list(dict_items), safe=False)


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
        current_dict = {'id': item.id, 'fields': [] }
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
