from django.urls import path
from library.views import AllSectionListView, ResourcesListView, AddResourceLikeView, DeleteResourceLikeView, \
    AddResourceFavoriteListView, DeleteResourceFavoriteListView, FavoriteResourceCountView, AdvicesListView, \
    AdviceItemListView, ResourceItemListView, FavoriteResourcesListView, FavoriteAdvicesListView

app_name = 'library'

urlpatterns = [
    path('sections/', AllSectionListView.as_view(), name='section'),
    path('<int:pk>/resources/', ResourcesListView.as_view({'get': 'grouped_by_section'}), name='resources'),
    path('advices/', AdvicesListView.as_view(), name='advices'),
    path('resource/<int:pk>/', ResourceItemListView.as_view(), name='resource'),
    path('advice/<int:pk>/', AdviceItemListView.as_view(), name='advice'),


    path('like/add/', AddResourceLikeView.as_view(), name='section_add_like'),
    path('like/delete/', DeleteResourceLikeView.as_view(), name='section_delete_like'),

    path('favorite/add/', AddResourceFavoriteListView.as_view(), name='section_add_favorite'),
    path('favorite/delete/', DeleteResourceFavoriteListView.as_view(), name='section_delete_favorite'),
    path('favorite/count/', FavoriteResourceCountView.as_view(), name='favorite_count'),

    path('favorite/<int:pk>/resources/', FavoriteResourcesListView.as_view({'get': 'grouped_by_section'}), name='favorite_resources'),
    path('favorite/advice/', FavoriteAdvicesListView.as_view(),name='favorite_advice'),

]