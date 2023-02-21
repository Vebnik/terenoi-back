from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from authapp.models import User, Group
from finance.models import StudentBalance, StudentSubscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubscription
        fields = ('title', 'id')


class StudentBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentBalance
        fields = ('money_balance', 'lessons_balance',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('title', 'status', 'teacher',)


class UserSerializers(serializers.ModelSerializer):

    group = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    status_color = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('fullname', 'status', 'avatar', 'group', 'balance', 'status_color', 'email', 'id',
                    'subscription', )

    def get_group(self, user: User):
        group = Group.objects.filter(students__in=[user])
        if group:
            return GroupSerializer(group.first()).data
        return None

    def get_fullname(self, user: User):
        return user.get_full_name()

    def get_balance(self, user: User):
        balance = StudentBalance.objects.filter(user=user).first()

        if balance:
            return StudentBalanceSerializer(balance).data
        return None


    def get_status_color(self, user: User):
        return user.get_status_color()

    def get_subscription(self, user: User):
        subscription = StudentSubscription.objects.filter(student=user, is_active=True).first()

        if subscription:
            return SubscriptionSerializer(subscription).data
        return None


class UserCreateSerializers(serializers.ModelSerializer):

    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField(required=False)
    gender = serializers.CharField()
    is_pass_generation = serializers.BooleanField()
    birth_date = serializers.CharField()
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('id', 'middle_name', 'last_name', 'first_name', 'avatar', 'email', 'phone', 'password', 'additional_user_number', 'birth_date', 
                    'gender', 'is_pass_generation', )