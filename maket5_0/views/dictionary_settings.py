from django.http import JsonResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0 import models


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def dictionary_settings(request):
    dictionary_structure = dictionary_menu_structure()
    return JsonResponse(dictionary_structure, safe=False)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def fields_structure(request):
    menu_structure = dictionary_menu_structure()
    fields = {}
    for clause in menu_structure:
        for dictionary in clause['contents']:
            current_class = getattr(models, dictionary['class'])
            fields.update({dictionary['class']: current_class.dictionary_fields()})
    return JsonResponse(fields, safe=False)


def dictionary_menu_structure():
    return [
        {
            'name': 'Продукция',
            'iconUrl': 'pen-to-square',
            'contents': [
                {
                    'name': 'Продукция',
                    'class': 'Good',
                    'emitChoices': True
                },
                {
                    'name': 'Детали',
                    'class': 'DetailItem',
                },
                {
                    'name': 'Наборы изображений',
                    'class': 'DetailImagesSet',
                    'emitChoices': True
                },
                {
                    'name': 'Типы деталей',
                    'class': 'DetailType',
                },
                {
                    'name': 'Изображения',
                    'class': 'DetailImage',
                },
            ]
        },
        {
            'name': 'Цвета',
            'iconUrl': 'paintbrush',
            'contents': [
                {
                    'name': 'Цветовая Схема',
                    'class': 'ColorScheme',
                },
                {
                    'name': 'Цвет',
                    'class': 'Color',
                },
                {
                    'name': 'Тип Материала',
                    'class': 'MaterialType',

                },
            ]
        },
        {
            'name': 'Печать',
            'iconUrl': 'paint-roller',
            'contents': [
                {
                    'name': 'Место печати (деталь)',
                    'class': 'PrintPlace',

                },
                {
                    'name': 'Ориентация печати',
                    'class': 'PrintPosition',
                },
                {
                    'name': 'Тип печати',
                    'class': 'PrintType',
                }
            ]
        },
        {
            'name': 'Клиенты',
            'iconUrl': 'sack-xmark',
            'contents': [
                {
                    'name': 'Тип группы',
                    'class': 'TypeGroup',
                },
                {
                    'name': 'Тип клиента',
                    'class': 'CustomerType',
                },
                {
                    'name': 'Группы клиентов',
                    'class': 'CustomerGroup',
                },
                {
                    'name': 'Клиенты',
                    'class': 'Customer',
                },
                {
                    'name': 'Менеджеры клиентов',
                    'class': 'Manager',
                },
            ]
        },
        {
            'name': 'География',
            'iconUrl': 'earth-africa',
            'contents': [
                {
                    'name': 'Федеральный округ',
                    'class': 'FedRegion',
                },
                {
                    'name': 'Регион — Федеральный округ',
                    'class': 'RegionToFedRegion',
                },
            ]
        },
        {
            'name': 'Прочие',
            'iconUrl': 'gear',
            'contents': [
                {
                    'name': 'Наши компании',
                    'class': 'OurCompany',
                },
            ]
        }
    ]
