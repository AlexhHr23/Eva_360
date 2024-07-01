from django.urls import path
from core.reports.views.quiz_report.views import *

urlpatterns = [
    path('quiz/', QuizReportView.as_view(), name='quiz_report'),
]
