from django.urls import path

from lessons.views import AllUserLessonsListView, UserLessonRetrieveView, VoxiTeacherInfoRetrieveView, \
    VoxiStudentInfoRetrieveView, UserLessonCreateView, LessonUserStatusUpdateView, AllUserClassesListView

app_name = 'lessons'

urlpatterns = [
    path('add/', UserLessonCreateView.as_view(), name='add_lessons'),
    path('all/', AllUserLessonsListView.as_view(), name='all_lessons'),
    path('<int:pk>/', UserLessonRetrieveView.as_view(), name='lesson'),
    path('classes/', AllUserClassesListView.as_view(), name='classes'),
    path('voxi-teacher-info/<int:pk>/', VoxiTeacherInfoRetrieveView.as_view(), name='voxi_teacher'),
    path('voxi-student-info/<int:pk>/', VoxiStudentInfoRetrieveView.as_view(), name='voxi_student'),
    path('user-status/update/<int:pk>/', LessonUserStatusUpdateView.as_view(), name='user_status_update')
]
