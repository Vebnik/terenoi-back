from rest_framework import serializers
from courses.models import Courses, LessonCourse, CourseWishList


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

    # TODO create permissions for materials

    class Meta:
        model = Courses
        fields = '__all__'

    def get_img(self, instance):
        return instance.get_course_img()

    def get_time_duration(self, instance):
        return instance.get_minutes()

    def get_author(self, instance):
        name = f'{instance.author.first_name} {instance.author.last_name}'
        return name


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

    # TODO create permissions for materials

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


class WishListSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = CourseWishList
        fields = ('count',)

    def get_count(self, instance):
        wish_count = CourseWishList.objects.filter(course__pk=int(self.context.get('pk'))).count()
        return wish_count
