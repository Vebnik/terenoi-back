from django.urls import path

from courses.views import AllCoursesListView, CoursesRetrieveView, LessonsCourseAllView, LessonCourseRetrieveView, \
    AddCourseWishListView, DeleteCourseWishListView, PurchasedCourseRetrieveView, AddCourseLikeView, \
    DeleteCourseLikeView, LikeView, WishListView

app_name = 'courses'

urlpatterns = [
    path('all/', AllCoursesListView.as_view(), name='all_courses'),
    path('<int:pk>/', CoursesRetrieveView.as_view(), name='course'),
    path('<int:pk>/lessons/', LessonsCourseAllView.as_view(), name='all_course_lessons'),
    path('lesson/<int:pk>/', LessonCourseRetrieveView.as_view(), name='course_lesson'),

    path('<int:pk>/like/', LikeView.as_view(), name='all_likes_in_course'),

    path('wishlist/', WishListView.as_view(), name='wishlist'),
    path('wishlist/add/', AddCourseWishListView.as_view(), name='add_wishlist'),
    path('wishlist/delete/', DeleteCourseWishListView.as_view(), name='delete_wishlist'),

    path('like/add/', AddCourseLikeView.as_view(), name='add_like'),
    path('like/delete/', DeleteCourseLikeView.as_view(), name='delete_like'),

    path('<int:pk>/buy/', PurchasedCourseRetrieveView.as_view(), name='course_buy'),
]
