from django.urls import path

from lessons.views import AllUserLessonsListView, UserLessonRetrieveView

app_name = 'lessons'

urlpatterns = [
    path('all/', AllUserLessonsListView.as_view(), name='all_lessons'),
    path('<int:pk>/', UserLessonRetrieveView.as_view(), name='lesson'),
]
