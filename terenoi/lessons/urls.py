from django.urls import path

from lessons.views import AllUserLessonsListView, UserLessonRetrieveView, VoxiTeacherInfoRetrieveView, \
    VoxiStudentInfoRetrieveView

app_name = 'lessons'

urlpatterns = [
    path('all/', AllUserLessonsListView.as_view(), name='all_lessons'),
    path('<int:pk>/', UserLessonRetrieveView.as_view(), name='lesson'),
    path('voxi-teacher-info/<int:pk>/', VoxiTeacherInfoRetrieveView.as_view(), name='voxi_teacher'),
    path('voxi-student-info/<int:pk>/', VoxiStudentInfoRetrieveView.as_view(), name='voxi_student')
]
