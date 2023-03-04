from django_filters import FilterSet, BooleanFilter
from django.db.models import Q

from authapp.models import User


class TeacherFreeFilter(FilterSet):
    """Фильтр для свободных учителей"""
    
    class Meta:
        model = User



class PublicationFilter(FilterSet):
    """Фильтр для публикаций"""
    free = BooleanFilter(method='free_filter', field_name='free')
    buy = BooleanFilter(method='for_buy_filter', field_name='buy')
    subscribe = BooleanFilter(method='for_subscribe_filter', field_name='subscribe')
    music = BooleanFilter(method='music_filter', field_name='music')
    photo = BooleanFilter(method='photo_filter', field_name='photo')
    video = BooleanFilter(method='video_filter', field_name='video')
    article = BooleanFilter(method='article_filter', field_name='article')

    @classmethod
    def free_filter(cls, queryset, _, value):
        if value:
            return queryset.filter(if_free=True)
        return queryset

    @classmethod
    def for_buy_filter(cls, queryset, _, value):
        if value:
            return queryset.filter(
                Q(if_free=False) &
                Q(
                    Q(price__gt=0) | Q(price_btc__gt=0) | Q(price_eth__gt=0)
                )
            )
        return queryset

    @classmethod
    def for_subscribe_filter(cls, queryset, _, value):
        if value:
            return queryset.filter(
                if_free=False, price=0, price_btc=0, price_eth=0)
        return queryset

    @classmethod
    def music_filter(cls, queryset, _, value):
        if value:
            return queryset.exclude(audios__isnull=True)
        return queryset