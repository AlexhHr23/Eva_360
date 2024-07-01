import json

from django.http import HttpResponse
from django.views.generic import FormView

from core.erp.models import QuizAnswers, Quiz, QuizAnswersDetail
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class QuizReportView(ModuleMixin, FormView):
    form_class = ReportForm
    template_name = 'quiz_report/report.html'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search_report':
                users = []
                series = []
                id = request.POST['quiz']
                if len(id):
                    quiz = Quiz.objects.get(pk=id)
                    for i in QuizAnswers.objects.filter(quiz_id=quiz.id).order_by('id'):
                        item = i.toJSON()
                        item['answers'] = [d.toJSON() for d in i.quizanswersdetail_set.all()]
                        users.append(item)
                    for i in [0, 1, 2, 3, 4]:
                        count = QuizAnswersDetail.objects.filter(quiz_detail__quiz=quiz, answer=i).count()
                        series.append({'name': f'Respuesta {i}', 'y': count})
                data = {'users': users, 'series': series}
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Encuestas'
        return context
