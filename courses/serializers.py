from rest_framework import serializers
from courses.models import Courses, LessonCourse, CourseWishList, CourseLikeList, PurchasedCourses, \
    PurchasedCoursesRequest
from django.conf import settings


class CourseSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    time_duration = serializers.SerializerMethodField()

    class Meta:
        model = Courses
        fields = (
            'id', 'img', 'title', 'description', 'time_duration',)

    def get_img(self, instance):
        return instance.get_course_img()

    def get_time_duration(self, instance):
        return instance.get_minutes()


class CourseRetrieveSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    time_duration = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    materials = serializers.SerializerMethodField()
    is_purchased = serializers.SerializerMethodField()
    is_wishlist = serializers.SerializerMethodField()
    course_purchase_status = serializers.SerializerMethodField()

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

    def get_avatar(self, instance):
        user = instance.author
        return user.get_avatar()

    def get_time_duration(self, instance):
        return instance.get_minutes()

    def get_author(self, instance):
        name = f'{instance.author.first_name} {instance.author.last_name}'
        return name

    def get_materials(self, instance):
        return instance.get_materials()

    def get_is_purchased(self, instance):
        user = self._user()
        is_purchased = PurchasedCourses.objects.filter(user=user, course=instance)
        if is_purchased:
            return True
        return False

    def get_is_wishlist(self, instance):
        user = self._user()
        wish = CourseWishList.objects.filter(course=instance, user=user)
        if wish:
            return True
        return False

    def get_course_purchase_status(self, instance):
        user = self._user()
        request_purchase = PurchasedCoursesRequest.objects.filter(user=user, course=instance, is_resolved=False).first()
        if request_purchase:
            return True
        return False


class LessonsCourseAllSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    time_duration = serializers.SerializerMethodField()

    class Meta:
        model = LessonCourse
        fields = ('id', 'img', 'title', 'time_duration')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_img(self, instance):
        user = self._user()
        is_purchased = PurchasedCourses.objects.filter(user=user, course=instance.course)
        if is_purchased:
            return instance.get_lesson_img()
        else:
            from PIL import ImageFilter, Image
            from io import BytesIO
            with open(instance.img.path, 'rb') as img_file:
                img = Image.open(img_file)
                for _ in range(10):
                    blurred_image = img.filter(ImageFilter.GaussianBlur(radius=100))
                img_byte_arr = BytesIO()
                blurred_image.save(img_byte_arr, format=img.format)
                img_byte_arr = img_byte_arr.getvalue()
                path_list, path_list_return = instance.img.path, instance.img.url
                path_list, path_list_return = path_list.split('.'), path_list_return.split('.')
                path_blur_img, path_blur_img_return = f'{path_list[0]}-blur.{path_list[1]}', f'{path_list_return[0]}-blur.{path_list_return[1]}'
                with open(path_blur_img, 'wb') as img:
                    img.write(img_byte_arr)
                    return f'{settings.BACK_URL}{path_blur_img_return}'

    def get_time_duration(self, instance):
        return instance.get_minutes()


class LessonsCourseRetrieveSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    time_duration = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = LessonCourse
        fields = '__all__'

    def get_img(self, instance):
        return instance.get_lesson_img()

    def get_avatar(self, instance):
        user = instance.author
        return user.get_avatar()

    def get_video(self, instance):
        return instance.get_video()

    def get_time_duration(self, instance):
        return instance.get_minutes()

    def get_author(self, instance):
        name = f'{instance.author.first_name} {instance.author.last_name}'
        return name

    def get_materials(self, instance):
        return instance.get_materials()


class CourseLikeListSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = CourseLikeList
        fields = ('count', 'is_like')

    def get_count(self, instance):
        wish_count = CourseLikeList.objects.filter(course__pk=int(self.context.get('pk'))).count()
        return wish_count

    def get_is_like(self, instance):
        user = self.context.get('user')
        like = CourseLikeList.objects.filter(course__pk=int(self.context.get('pk')), user=user)
        if like:
            return True
        return False
