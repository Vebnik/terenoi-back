from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from authapp.models import User, Group, AdditionalUserNumber
from finance.models import StudentBalance, StudentSubscription, PaymentMethod
from profileapp.models import ManagerToUser


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


class AdditionalNumberSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdditionalUserNumber
        fields = ('phone', 'comment', )


class UserCreateUpdateSerializers(serializers.ModelSerializer):

    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField(required=False)
    gender = serializers.CharField()
    is_pass_generation = serializers.BooleanField()
    birth_date = serializers.CharField()
    avatar = Base64ImageField(required=False)
    additional_user_number = AdditionalNumberSerializers(many=True)
    manager_related = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'middle_name', 'last_name', 'first_name', 'avatar', 'email', 'phone', 'password', 
                    'birth_date', 'gender', 'is_pass_generation', 'additional_user_number', 
                    'manager_related', 'status')

    def update(self, instance: User, validated_data):
        user = instance

        if not user.is_staff:
            add_numbers = validated_data.pop('additional_user_number', [])
            manager_pk = self.context.get('request').data.get('manager_related')
            manager = User.objects.get(pk=manager_pk)

            m2s = ManagerToUser.objects.filter(user=user)

            if m2s: m2s.delete()

            ManagerToUser.objects.create(manager=manager, user=user)

            additional = []   
            for number in add_numbers:
                number['user_ref'] = user
                additional.append(AdditionalUserNumber.objects.create(**number))

            user.additional_user_number.set(additional)

        user.save()

        return super().update(user, validated_data)

    def create(self, validated_data):

        add_numbers = validated_data.pop('additional_user_number', [])
        manager_pk = self.context.get('request').data.get('manager_related')
        manager = User.objects.get(pk=manager_pk)
        user = User.objects.create(**validated_data)
        m2s = ManagerToUser.objects.filter(user=user)

        if m2s: m2s.delete()

        ManagerToUser.objects.create(manager=manager, user=user)

        additional = []    
        for number in add_numbers:
            number['user_ref'] = user
            additional.append(AdditionalUserNumber.objects.create(**number))

        user.additional_user_number.set(additional)
        user.save()

        return user

    def get_manager_related(self, user):
        try:
            return ManagerToUser.objects.filter(user=user).first().manager.pk
        except:
            return None


class SubscriptionListSerializers(serializers.ModelSerializer):

    payment_methods = serializers.SerializerMethodField()

    class Meta:
        model = StudentSubscription
        fields = ('id', 'payment_methods', 'title', 'plan_type', 'billing', 'lesson_count', 
                'lesson_duration', 'lesson_cost', 'subscription_cost', 'student')

    def get_payment_methods(self, instance):
        try:
            return { 'title': instance.payment_methods.title, }
        except:
            return { 'title': None }


class UserDetailSerializers(serializers.ModelSerializer):
    
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    gender = serializers.CharField()
    birth_date = serializers.CharField()
    manager_related = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'middle_name', 'last_name', 'first_name', 'avatar', 'email', 'phone', 
                'birth_date', 'gender', 'manager_related', 'status', 'subscription', 'role')

    def get_manager_related(self, user):
        try:
            manager = ManagerToUser.objects.filter(user=user).first().manager
            return { 'pk': manager.pk, 'name': manager.get_full_name() }
        except:
            return None

    def get_subscription(self, instance):
        # TODO У подписок может быть несколько Учеников ????
        # TODO Уточнить момент

        try:
            sub_serializes = SubscriptionListSerializers(StudentSubscription.objects.filter(student=instance).first())
            return sub_serializes.data
        except Exception as ex:
            print(ex)
            return None

    def get_role(self, instance):
        return instance.get_role()


class StudentStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('status', )


class ManagerListSerializers(serializers.ModelSerializer):

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'fullname')

    def get_fullname(self, instance: User):
        try:
            return instance.get_full_name()
        except Exception as ex:
            return 'Empty'