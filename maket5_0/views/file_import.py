import os

from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

fs_tmp = FileSystemStorage(location='maket5_0/files')


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def import_file(request):
    try:
        os.remove('maket5_0/files/tmp_file')
    except:
        pass
    file = request.FILES['tmp_file']
    try:
        fs_tmp.save('tmp_file', file)
        result = True
    except:
        result = False
    return Response({'result': result})
