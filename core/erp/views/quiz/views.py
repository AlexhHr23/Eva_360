import json

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, FormView

from core.erp.choices import STATUS_QUIZ_ANSWERS
from core.erp.forms import Quiz, QuizForm
from core.erp.models import Question, QuizDetail, QuizAnswers, QuizAnswersDetail
from core.security.mixins import PermissionMixin


class QuizListView(PermissionMixin, TemplateView):
    template_name = 'quiz/admin/list.html'
    permission_required = 'view_quiz'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Quiz.objects.all().order_by('id'):
                    data.append(i.toJSON())
            elif action == 'search_questions':
                data = []
                for i in QuizDetail.objects.filter(quiz_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'activate_quiz':
                quiz = Quiz.objects.get(pk=request.POST['id'])
                quiz.state = True
                quiz.save()
                quiz.activate_quiz()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('quiz_create')
        context['title'] = 'Listado de Encuestas'
        return context


class QuizCreateView(PermissionMixin, CreateView):
    model = Quiz
    template_name = 'quiz/admin/create.html'
    form_class = QuizForm
    success_url = reverse_lazy('quiz_list')
    permission_required = 'add_quiz'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    quiz = Quiz()
                    quiz.instructions = request.POST['instructions']
                    quiz.type = request.POST['type']
                    quiz.name = request.POST['name']
                    quiz.save()
                    for i in json.loads(request.POST['questions']):
                        detail = QuizDetail()
                        detail.quiz_id = quiz.id
                        detail.question_id = int(i['id'])
                        detail.save()
            elif action == 'search_questions':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                queryset = Question.objects.filter().exclude(id__in=ids).order_by('description')
                if len(term):
                    queryset = queryset.filter(description__icontains=term)
                    queryset = queryset[0:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Encuesta'
        context['action'] = 'add'
        context['questions'] = []
        return context


class QuizUpdateView(PermissionMixin, UpdateView):
    model = Quiz
    template_name = 'quiz/admin/create.html'
    form_class = QuizForm
    success_url = reverse_lazy('quiz_list')
    permission_required = 'change_quiz'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.state:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    quiz = self.get_object()
                    quiz.instructions = request.POST['instructions']
                    quiz.type = request.POST['type']
                    quiz.name = request.POST['name']
                    quiz.save()
                    quiz.quizdetail_set.all().delete()
                    for i in json.loads(request.POST['questions']):
                        detail = QuizDetail()
                        detail.quiz_id = quiz.id
                        detail.question_id = int(i['id'])
                        detail.save()
            elif action == 'search_questions':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                queryset = Question.objects.filter().exclude(id__in=ids).order_by('description')
                if len(term):
                    queryset = queryset.filter(description__icontains=term)
                    queryset = queryset[0:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_questions(self):
        data = []
        for i in self.get_object().quizdetail_set.all():
            data.append(i.question.toJSON())
        return json.dumps(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Encuesta'
        context['action'] = 'edit'
        context['questions'] = self.get_questions()
        return context


class QuizDeleteView(PermissionMixin, DeleteView):
    model = Quiz
    template_name = 'quiz/admin/delete.html'
    success_url = reverse_lazy('quiz_list')
    permission_required = 'delete_quiz'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class QuizUserListView(PermissionMixin, TemplateView):
    template_name = 'quiz/user/list.html'
    permission_required = 'view_quiz_user'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset = QuizAnswers.objects.filter(user_id=request.user.id).order_by('id')
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_questions':
                data = []
                for i in QuizAnswersDetail.objects.filter(quiz_answers_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Encuestas'
        return context


class QuizAnswersView(PermissionMixin, FormView):
    template_name = 'quiz/user/create.html'
    form_class = QuizForm
    success_url = reverse_lazy('quiz_user_list')
    permission_required = 'add_quiz_user'

    def get(self, request, *args, **kwargs):
        if self.get_object() is None:
            messages.error(request, 'La encuesta solicitada no existe o esta inactiva')
            return HttpResponseRedirect(self.success_url)
        return super(QuizAnswersView, self).get(request, *args, **kwargs)

    def get_object(self):
        queryset = QuizAnswers.objects.filter(status=STATUS_QUIZ_ANSWERS[0][0], quiz__access_key=self.kwargs['access_key'], user_id=self.request.user.id)
        if queryset.exists():
            return queryset[0]
        return None

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    quiz_answers = self.get_object()
                    quiz_answers.status = STATUS_QUIZ_ANSWERS[1][0]
                    quiz_answers.save()
                    for i in json.loads(request.POST['answers']):
                        detail = QuizAnswersDetail.objects.get(pk=i['id'])
                        detail.answer = i['answer']
                        detail.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Encuesta'
        context['action'] = 'add'
        context['instance'] = self.get_object()
        context['questions'] = []
        return context
