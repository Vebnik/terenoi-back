from django.urls import path

from lessons.views import AllUserLessonsListView, UserLessonRetrieveView, VoxiTeacherInfoRetrieveView, \
    VoxiStudentInfoRetrieveView, UserLessonCreateView, LessonUserStatusUpdateView, AllUserClassesListView, \
    LessonUpdateView, LessonMaterialsAdd, LessonHomeworksAdd, LessonMaterialsRetrieveView, LessonHomeworksRetrieveView, \
    LessonEvaluationRetrieveView, LessonEvaluationUpdateView, CreateVoxiCallData, LessonTransferUpdateView, \
    LessonEvaluationQuestionsRetrieveView, LessonRateHomeworksAdd, LessonRateHomeworkRetrieveView, HomepageListView, \
    StudentsListView, StudentsRejectView, StudentsDetailView, HomeworksView, TopicUpdateView, PurposeUpdateView

app_name = 'lessons'

urlpatterns = [
    path('add/', UserLessonCreateView.as_view(), name='add_lessons'),
    path('all/', AllUserLessonsListView.as_view(), name='all_lessons'),
    path('update/<int:pk>/', LessonUpdateView.as_view(), name='update_lesson'),
    path('<int:pk>/', UserLessonRetrieveView.as_view(), name='lesson'),
    path('classes/', AllUserClassesListView.as_view(), name='classes'),

    path('students/', StudentsListView.as_view(), name='students'),
    path('students/<int:pk>/', StudentsDetailView.as_view(), name='students_detail'),
    path('students/<int:pk>/update/topic/', TopicUpdateView.as_view(), name='students_update_topic'),
    path('students/<int:pk>/update/purpose/', PurposeUpdateView.as_view(), name='students_update_purpose'),
    path('homeworks/', HomeworksView.as_view(), name='homeworks'),
    path('reject-student/<int:pk>/', StudentsRejectView.as_view(), name='reject_student'),

    path('transfer/<int:pk>/', LessonTransferUpdateView.as_view(), name='lesson_transfer'),

    path('homepage/', HomepageListView.as_view(), name='homepage'),

    path('materials/add/<int:pk>/', LessonMaterialsAdd.as_view(), name='materials_add'),
    path('homeworks/add/<int:pk>/', LessonHomeworksAdd.as_view(), name='homeworks_add'),
    path('materials/<int:pk>/', LessonMaterialsRetrieveView.as_view(), name='lesson_materials'),
    path('homeworks/<int:pk>/', LessonHomeworksRetrieveView.as_view(), name='lesson_homeworks'),
    path('rate/add/<int:pk>/', LessonRateHomeworksAdd.as_view(), name='rate_homework_add'),
    path('rate/<int:pk>/', LessonRateHomeworkRetrieveView.as_view(), name='homework_rate'),

    path('evaluation/<int:pk>/', LessonEvaluationRetrieveView.as_view(), name='lesson_evaluation'),
    path('evaluation-questions/<int:pk>/', LessonEvaluationQuestionsRetrieveView.as_view(),
         name='evaluation-questions'),
    path('evaluation/add/<int:pk>/', LessonEvaluationUpdateView.as_view(), name='lesson_user_evaluation_add'),

    path('voxi-teacher-info/<int:pk>/', VoxiTeacherInfoRetrieveView.as_view(), name='voxi_teacher'),
    path('voxi-student-info/<int:pk>/', VoxiStudentInfoRetrieveView.as_view(), name='voxi_student'),
    path('user-status/update/<int:pk>/', LessonUserStatusUpdateView.as_view(), name='user_status_update'),
    path('voxi-call-data/', CreateVoxiCallData.as_view(), name='voxi_call_data')
]
