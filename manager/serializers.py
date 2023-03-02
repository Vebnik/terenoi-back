from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from dateutil.rrule import rrule, WEEKLY
from dateutil.parser import parse
import calendar

from authapp.models import User, Group, AdditionalUserNumber
from finance.models import StudentBalance, StudentSubscription, PaymentMethod
from profileapp.models import ManagerToUser, Subject
from lessons.models import Schedule, ScheduleSettings


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
        fields = ('id', 'title', 'status', 'teacher')


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


class ScheduleSettingsSerializers(serializers.ModelSerializer):

    shedule = serializers.SerializerMethodField()

    class Meta:
        model = ScheduleSettings
        fields = ('id','shedule','lesson_duration','count','near_lesson','last_lesson')

    def get_shedule(self, instance):
        shedule: Schedule = instance.shedule

        return {
            'id': shedule.pk,
            'title': shedule.title,
            'teacher': shedule.teacher.pk,
            'subject': shedule.subject.pk,
            'weekday': [item.pk for item in shedule.weekday.all()],
            'group': {
                'id': shedule.group.pk,
                'title': shedule.group.title,
            },
        }


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
    schedule_settings = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'middle_name', 'last_name', 'first_name', 'avatar', 'email', 'phone', 
                'birth_date', 'gender', 'manager_related', 'status', 'subscription', 'role',
                'schedule_settings', )

    def get_manager_related(self, user):
        try:
            manager = ManagerToUser.objects.filter(user=user).first().manager
            return { 'pk': manager.pk, 'name': manager.get_full_name() }
        except:
            return None

    def get_subscription(self, instance):
        try:
            sub_serializes = SubscriptionListSerializers(
                StudentSubscription.objects.filter(student=instance).first()
            )
            return sub_serializes.data
        except Exception as ex:
            print(ex)
            return None

    def get_schedule_settings(self, instance: User):
        try:
            schedule = ScheduleSettings.objects.get(shedule__group__students__in=[instance.pk])
            return ScheduleSettingsSerializers(schedule).data
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


class TeacherListSerializers(serializers.ModelSerializer):

    fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'fullname')

    def get_fullname(self, instance: User):
        return instance.get_full_name()


class SubjectListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')


class ScheduleCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('title', 'teacher', 'subject', 'weekday')

    def save(self):
        full_data: dict = self.initial_data

        date_range = rrule(
            freq=WEEKLY, 
            dtstart=parse(f"{full_data.get('lessons_range')[0]} {full_data.get('time')}"),
            until=parse(f"{full_data.get('lessons_range')[1]} {full_data.get('time')}"),
            wkst=calendar.firstweekday(),
            byweekday=[*map(int, full_data.get('weekday'))]
        )
        
        if not Group.objects.filter(title=full_data.get('title')):
            group = Group(
                title=full_data.get('title'),
                description=f'Индивидуальная группа для ученика {full_data.get("user")}',
                teacher=User.objects.get(pk=full_data.get('teacher')),
            ); group.save(); group.students.set([User.objects.get(pk=full_data.get('user'))])
        else:
            group = Group.objects.get(title=full_data.get('title'))

        schedule = super().save()
        schedule.group = group

        scheduleSettings = ScheduleSettings(
            count=len([*date_range]),
            shedule=schedule,
            lesson_duration=full_data.get('lesson_duration'),
            near_lesson=parse(f"{full_data.get('lessons_range')[0]} {full_data.get('time')}"),
            last_lesson=parse(f"{full_data.get('lessons_range')[1]} {full_data.get('time')}")
        ); scheduleSettings.save(); schedule.save()

        return schedule


class ScheduleGroupCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('title', 'teacher', 'subject', 'weekday')

    def save(self, **kwargs):
        full_data: dict = self.initial_data

        date_range = rrule(
            freq=WEEKLY, 
            dtstart=parse(f"{full_data.get('lessons_range')[0]} {full_data.get('time')}"),
            until=parse(f"{full_data.get('lessons_range')[1]} {full_data.get('time')}"),
            wkst=calendar.firstweekday(),
            byweekday=[*map(int, full_data.get('weekday'))]
        )

        group = Group(
            title=full_data.get('title'),
            description=f'Индивидуальная группа для ученика {full_data.get("user")}',
            teacher=User.objects.get(pk=full_data.get('teacher')),
        ); group.save(); group.students.set([User.objects.get(pk=full_data.get('user'))])
        
        schedule = super().save()
        schedule.group = group

        scheduleSettings = ScheduleSettings(
            count=len([*date_range]),
            shedule=schedule,
            lesson_duration=full_data.get('lesson_duration'),
            near_lesson=parse(f"{full_data.get('lessons_range')[0]} {full_data.get('time')}"),
            last_lesson=parse(f"{full_data.get('lessons_range')[1]} {full_data.get('time')}")
        ); scheduleSettings.save(); schedule.save()

        return schedule