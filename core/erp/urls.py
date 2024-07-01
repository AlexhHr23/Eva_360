from django.urls import path
from core.erp.views.student.views import *
from core.erp.views.teacher.views import *
from core.erp.views.category.views import *
from core.erp.views.question.views import *
from core.erp.views.quiz.views import *

urlpatterns = [
    # student
    path('student/', StudentListView.as_view(), name='student_list'),
    path('student/add/', StudentCreateView.as_view(), name='student_create'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),
    path('student/delete/<int:pk>/', StudentDeleteView.as_view(), name='student_delete'),
    path('student/update/profile/', StudentUpdateProfileView.as_view(), name='student_update_profile'),
    # teacher
    path('teacher/', TeacherListView.as_view(), name='teacher_list'),
    path('teacher/add/', TeacherCreateView.as_view(), name='teacher_create'),
    path('teacher/update/<int:pk>/', TeacherUpdateView.as_view(), name='teacher_update'),
    path('teacher/delete/<int:pk>/', TeacherDeleteView.as_view(), name='teacher_delete'),
    path('teacher/update/profile/', TeacherUpdateProfileView.as_view(), name='teacher_update_profile'),
    # category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # question
    path('question/', QuestionListView.as_view(), name='question_list'),
    path('question/add/', QuestionCreateView.as_view(), name='question_create'),
    path('question/update/<int:pk>/', QuestionUpdateView.as_view(), name='question_update'),
    path('question/delete/<int:pk>/', QuestionDeleteView.as_view(), name='question_delete'),
    # quiz
    path('quiz/', QuizListView.as_view(), name='quiz_list'),
    path('quiz/add/', QuizCreateView.as_view(), name='quiz_create'),
    path('quiz/update/<int:pk>/', QuizUpdateView.as_view(), name='quiz_update'),
    path('quiz/delete/<int:pk>/', QuizDeleteView.as_view(), name='quiz_delete'),
    # quiz/user
    path('quiz/user/', QuizUserListView.as_view(), name='quiz_user_list'),
    path('quiz/user/answers/<str:access_key>/', QuizAnswersView.as_view(), name='quiz_answers'),
]
