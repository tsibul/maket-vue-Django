# from django.http import JsonResponse, HttpResponseBadRequest
# from django.shortcuts import redirect
# from django.contrib.auth import login, logout, authenticate
# from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# @csrf_exempt
# def custom_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             response = {
#                 'user_info': {
#                     'username': username,
#                     'firstName': request.user.first_name,
#                     'lastName': request.user.last_name,
#                     'groups': list(request.user.groups.values_list('name', flat=True)),
#                     'isSuperuser': request.user.is_superuser,
#                 }}
#             return JsonResponse(response, safe=False)
#         else:
#             return HttpResponseBadRequest('Неверное имя пользователя или пароль')
#
#     # Обработка других методов HTTP, если это необходимо
#     return HttpResponseBadRequest('Неверный метод запроса')
#
#
# @csrf_exempt
# def custom_logout(request):
#     logout(request)
#     return redirect('/marketing')


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class LogStatusView(APIView):
    def get(self, request):
        user = request.user

        response_data = {
            'username': user.username,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'isSuperUser': user.is_superuser,
        }

        if user.groups:
            user_groups = [group.name for group in user.groups.all()]
            response_data['groups'] = user_groups

        return Response(response_data)