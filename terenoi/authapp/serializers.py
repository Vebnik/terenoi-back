from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authapp.models import User, VoxiAccount
from profileapp.models import ReferralPromo
from profileapp.services import generateRefPromo
from settings.models import UserCity


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
        user = User.objects.create_user(username=self.validated_data['username'], email=self.validated_data['email'],
                                        password=self.validated_data['password'])
        ref = ReferralPromo.objects.filter(user=user).first()
        if ref:
            if self.context.get('request').data.get('referral'):
                ref.from_user_link = self.context.get('request').data.get('referral')
                ref.save()
        else:
            promo = generateRefPromo()
            ReferralPromo.objects.create(user=user, user_link=promo)

        user_city = UserCity.objects.filter(user=user).first()
        if not user_city:
            UserCity.objects.create(user=user)

        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    """
    remember = serializers.BooleanField(default=False)

    def get_token(self, user):
        token = super(UserLoginSerializer, self).get_token(user)
        access_token = token.access_token
        flag = self._kwargs['data'].get('remember', False)
        if flag:
            access_token.set_exp(lifetime=datetime.timedelta(days=7))
        else:
            access_token.set_exp(lifetime=datetime.timedelta(hours=1))
        return token
    """

    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        user_obj = User.objects.filter(Q(email=attrs.get("username")) & Q(is_verified=True)).first()
        if user_obj:
            credentials['username'] = user_obj.username
        return super().validate(credentials)


class VerifyEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('token',)


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class VoxiAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoxiAccount
        fields = ('voxi_username', 'voxi_password')
