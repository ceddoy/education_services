from django.contrib.auth import password_validation
from rest_framework.serializers import ModelSerializer

from userapp.models import User


class UserModelSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {'password': {'write_only': True}, }

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
