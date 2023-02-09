from rest_framework import serializers
from courses.models import Courses, LessonCourse


class CourseSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = (
            'pk', 'img', 'title', 'description', 'time_duration',)

    def get_img(self, instance):
        return instance.get_course_img()


class CourseRetrieveSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    # TODO create permissions for materials

    class Meta:
        model = Courses
        fields = '__all__'

    def get_img(self, instance):
        return instance.get_course_img()


class LessonsCourseAllSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = LessonCourse
        fields = ('pk', 'img', 'title', 'time_duration')

    def get_img(self, instance):
        return instance.get_lesson_img()


class LessonsCourseRetrieveSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    # TODO create permissions for materials

    class Meta:
        model = Courses
        fields = '__all__'

    def get_img(self, instance):
        return instance.get_lesson_img()

    def get_video(self,instance):
        return instance.get_video()