from rest_framework import serializers

from authapp.models import User
from courses.models import Courses, LessonCourse, CourseWishList, CourseLikeList, PurchasedCourses


class CourseSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    time_duration = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = (
            'pk', 'img', 'title', 'description', 'time_duration',)

    def get_img(self, instance):
        return instance.get_course_img()

    def get_time_duration(self, instance):
        return instance.get_minutes()


class CourseRetrieveSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    time_duration = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = '__all__'

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_img(self, instance):
        return instance.get_course_img()

    def get_time_duration(self, instance):
        return instance.get_minutes()

    def get_author(self, instance):
        name = f'{instance.author.first_name} {instance.author.last_name}'
        return name

    def get_materials(self, instance):
        user = self._user()
        is_purchased = PurchasedCourses.objects.filter(user=user, course=instance)
        if is_purchased:
            return instance.get_materials()
        return None


class LessonsCourseAllSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    time_duration = serializers.SerializerMethodField()

    class Meta:
        model = LessonCourse
        fields = ('pk', 'img', 'title', 'time_duration')

    def get_img(self, instance):
        return instance.get_lesson_img()

    def get_time_duration(self, instance):
        return instance.get_minutes()


class LessonsCourseRetrieveSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    time_duration = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = LessonCourse
        fields = '__all__'

    def get_img(self, instance):
        return instance.get_lesson_img()

    def get_video(self, instance):
        return instance.get_video()

    def get_time_duration(self, instance):
        return instance.get_minutes()

    def get_author(self, instance):
        name = f'{instance.author.first_name} {instance.author.last_name}'
        return name

    def get_materials(self, instance):
        user = self._user()
        is_purchased = PurchasedCourses.objects.filter(user=user, course=instance.course)
        if is_purchased:
            return instance.get_materials()
        return None


class CourseLikeListSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    is_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = CourseLikeList
        fields = ('count', 'is_like', 'is_wishlist')

    def get_count(self, instance):
        wish_count = CourseLikeList.objects.filter(course__pk=int(self.context.get('pk'))).count()
        return wish_count

    def get_is_like(self, instance):
        user = self.context.get('user')
        like = CourseLikeList.objects.filter(course__pk=int(self.context.get('pk')), user=user)
        if like:
            return True
        return False

    def get_is_wishlist(self, instance):
        user = self.context.get('user')
        wish = CourseWishList.objects.filter(course__pk=int(self.context.get('pk')), user=user)
        if wish:
            return True
        return False
