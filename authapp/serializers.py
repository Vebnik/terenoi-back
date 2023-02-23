from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authapp.models import User, UserStudyLanguage, StudyLanguage, Group
from authapp.services.auth import find_username_by_phone_or_email
from finance.models import TeacherBankData
from profileapp.models import ReferralPromo
from profileapp.services import generateRefPromo
from settings.models import UserCity, CityTimeZone


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
        email = attrs['email']
        user_emails = User.objects.filter(email=email)
        if user_emails:
            raise serializers.ValidationError("Такой эмейл уже существует")
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
        city = CityTimeZone.objects.first()
        if not user_city:
            UserCity.objects.create(user=user, city=city)

        if user.is_teacher:
            bank = TeacherBankData.objects.filter(user=user).first()
            if not bank:
                TeacherBankData.objects.create(user=user)
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
            'username': find_username_by_phone_or_email(attrs.get("username")),
            'password': attrs.get("password")
        }
        return super().validate(credentials)


class VerifyEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('token',)


class UserNameSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'student_class')

    def get_avatar(self, instance):
        return instance.get_avatar()


class ProfileStudentDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'is_student')

    def get_avatar(self, instance):
        return instance.get_avatar()


class ProfileTeacherDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'is_teacher')

    def get_avatar(self, instance):
        return instance.get_avatar()


class StudyLanguageSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = StudyLanguage
        fields = ('name', 'status')

    def get_status(self, instance):
        user_lang = UserStudyLanguage.objects.filter(user=self.context.get('user')).first()
        if not user_lang:
            return False
        elif instance in user_lang.language.all():
            return True
        else:
            return False


class DataManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'telegram', 'whatsapp')


class UserFullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('students',)


class UserWhoiAmSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'fullname', 'is_staff', )

    def get_fullname(self, user: User):
        return user.get_full_name()