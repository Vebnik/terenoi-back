from rest_framework import serializers

from authapp.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    re_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 're_password')

    def validate(self, attrs):
        password = attrs['password']
        re_password = attrs['re_password']
        if password != re_password:
            raise serializers.ValidationError("Пароли не совпадают!")
        return attrs

    def save(self):
        print(self.validated_data)
        user = User.objects.create_user(username=self.validated_data['username'], email=self.validated_data['email'],
                                        password=self.validated_data['password'])
        return user


class VerifyEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('token',)


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


