from django.contrib import admin

from library.models import Language, LevelLanguage, Section, Resource, ResourceLikeList, ResourceFavoriteList


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')


@admin.register(LevelLanguage)
class LevelLanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'name')
    list_filter = ('language',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_section')
    list_filter = ('parent_section',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'language')
    list_filter = ('section',)


@admin.register(ResourceLikeList)
class ResourceLikeListAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource')


@admin.register(ResourceFavoriteList)
class ResourceFavoriteListAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource')
