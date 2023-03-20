from rest_framework import serializers
from library.models import Section, Resource, Language, LevelLanguage, ResourceLikeList, ResourceFavoriteList


class ChildSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = (
            'id', 'name')


class LevelLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelLanguage
        fields = (
            'id', 'name')


class LanguageSerializer(serializers.ModelSerializer):
    language_level = serializers.SerializerMethodField()

    class Meta:
        model = Language
        fields = (
            'id', 'name', 'language_level')

    def get_language_level(self, instance):
        language_level = LevelLanguage.objects.filter(language=instance)
        serializer = LevelLanguageSerializer(language_level, many=True)
        return serializer.data


class AllSectionSerializer(serializers.ModelSerializer):
    child_sections = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = (
            'id', 'name', 'description', 'language', 'child_sections',)

    def get_language(self, instance):
        sections = Section.objects.filter(parent_section=instance)
        for section in sections:
            resource = Resource.objects.filter(section=section)
            if resource:
                language_values = resource.values('language').distinct('language')
                language_list = [Language.objects.get(pk=item.get('language')) for item in language_values]
                serializer = LanguageSerializer(language_list, many=True)
                return serializer.data
        return None

    def get_child_sections(self, instance):
        sections = Section.objects.filter(parent_section=instance).select_related()
        serializer = ChildSectionSerializer(sections, many=True)
        return serializer.data


class SectionResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = (
            'id', 'name', 'description')


class ResourcesSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = (
            'id',
            'title',
            'description',
            'preview',
            'is_like',
            'like_count',
            'is_favorite')

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_preview(self, instance):
        return instance.get_preview()

    def get_is_like(self, instance):
        user = self._user()
        res = ResourceLikeList.objects.filter(user=user, resource=instance)
        if res:
            return True
        return False

    def get_like_count(self, instance):
        count = ResourceLikeList.objects.filter(resource=instance).count()
        return count

    def get_is_favorite(self, instance):
        user = self._user()
        fav = ResourceFavoriteList.objects.filter(user=user, resource=instance)
        if fav:
            return True
        return False


class AdvicesSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = (
            'id',
            'title',
            'description',
            'preview',
            'author_name',
            'link_resource',
            'label_resource',
            'is_like',
            'like_count',
            'is_favorite'
        )

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_preview(self, instance):
        return instance.get_preview()

    def get_author_name(self, instance):
        return f'{instance.user.first_name} {instance.user.last_name}'

    def get_is_like(self, instance):
        user = self._user()
        res = ResourceLikeList.objects.filter(user=user, resource=instance)
        if res:
            return True
        return False

    def get_like_count(self, instance):
        count = ResourceLikeList.objects.filter(resource=instance).count()
        return count

    def get_is_favorite(self, instance):
        user = self._user()
        fav = ResourceFavoriteList.objects.filter(user=user, resource=instance)
        if fav:
            return True
        return False


class ResourceItemSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = (
            'id',
            'title',
            'description',
            'preview',
            'link_video',
            'link_resource',
            'label_resource',
            'tags',
            'is_like',
            'like_count',
            'is_favorite'
        )

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_preview(self, instance):
        return instance.get_preview()

    def get_is_like(self, instance):
        user = self._user()
        res = ResourceLikeList.objects.filter(user=user, resource=instance)
        if res:
            return True
        return False

    def get_like_count(self, instance):
        count = ResourceLikeList.objects.filter(resource=instance).count()
        return count

    def get_is_favorite(self, instance):
        user = self._user()
        fav = ResourceFavoriteList.objects.filter(user=user, resource=instance)
        if fav:
            return True
        return False


class AdviceItemSerializer(serializers.ModelSerializer):
    preview = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = (
            'id',
            'title',
            'author_name',
            'description',
            'preview',
            'link_video',
            'link_resource',
            'label_resource',
            'is_like',
            'like_count',
            'is_favorite'
        )

    def _user(self):
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_preview(self, instance):
        return instance.get_preview()

    def get_author_name(self, instance):
        return f'{instance.user.first_name} {instance.user.last_name}'

    def get_is_like(self, instance):
        user = self._user()
        res = ResourceLikeList.objects.filter(user=user, resource=instance)
        if res:
            return True
        return False

    def get_like_count(self, instance):
        count = ResourceLikeList.objects.filter(resource=instance).count()
        return count

    def get_is_favorite(self, instance):
        user = self._user()
        fav = ResourceFavoriteList.objects.filter(user=user, resource=instance)
        if fav:
            return True
        return False
