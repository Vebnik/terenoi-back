from django.urls import path

from lessons.views import AllUserLessonsListView, UserLessonRetrieveView, VoxiTeacherInfoRetrieveView, \
    VoxiStudentInfoRetrieveView, UserLessonCreateView, LessonUserStatusUpdateView, AllUserClassesListView, \
    LessonUpdateView, LessonMaterialsAdd, LessonHomeworksAdd, LessonMaterialsRetrieveView, LessonHomeworksRetrieveView, \
    CreateVoxiCallData

app_name = 'lessons'

urlpatterns = [
    path('add/', UserLessonCreateView.as_view(), name='add_lessons'),
    path('all/', AllUserLessonsListView.as_view(), name='all_lessons'),
    path('update/<int:pk>/', LessonUpdateView.as_view(), name='update_lesson'),
    path('<int:pk>/', UserLessonRetrieveView.as_view(), name='lesson'),
    path('classes/', AllUserClassesListView.as_view(), name='classes'),

    path('materials/add/<int:pk>/', LessonMaterialsAdd.as_view(), name='materials_add'),
    path('homeworks/add/<int:pk>/', LessonHomeworksAdd.as_view(), name='homeworks_add'),
    path('materials/<int:pk>/', LessonMaterialsRetrieveView.as_view(), name='lesson_materials'),
    path('homeworks/<int:pk>/', LessonHomeworksRetrieveView.as_view(), name='lesson_homeworks'),

    path('voxi-teacher-info/<int:pk>/', VoxiTeacherInfoRetrieveView.as_view(), name='voxi_teacher'),
    path('voxi-student-info/<int:pk>/', VoxiStudentInfoRetrieveView.as_view(), name='voxi_student'),
    path('user-status/update/<int:pk>/', LessonUserStatusUpdateView.as_view(), name='user_status_update'),
    path('voxi-call-data/', CreateVoxiCallData.as_view(), name='voxi_call_data')
]
