import pathlib

from django.http import FileResponse
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from maket5_0.models import Pattern


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def pattern_show(request, file_pk, file_name):
    """
    Show pattern if it pdf, and download it in other cases
    :param request: pattern_show/<int:file_pk>
    :param file_pk: additional file id
    :return: file with file name
    """
    file = Pattern.objects.get(id=file_pk)
    file_type = pathlib.Path(str(file.file.name)).suffix
    if file_type == '.pdf':
        content_type ='application/pdf'
    else:
        content_type ='application/force-download'
    try:
        return FileResponse(open(file.file.path, 'rb'), content_type=content_type)
    except:
        return None
