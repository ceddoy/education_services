from django.contrib.auth import password_validation, authenticate
from rest_framework import serializers

from userapp.models import User


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {'password': {'write_only': True}, }

    def validate_password(self, value: str) -> str:
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        style={'input_type': 'email'},
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label="Token",
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
