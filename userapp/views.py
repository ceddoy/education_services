from rest_framework.generics import CreateAPIView

from userapp.models import User
from userapp.permissions import ForNotAuthUserPermission
from userapp.serializer import UserModelSerializer


class CreateUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = [ForNotAuthUserPermission, ]
