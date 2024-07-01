import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import Question, QuestionForm
from core.security.mixins import PermissionMixin


class QuestionListView(PermissionMixin, ListView):
    model = Question
    template_name = 'question/list.html'
    permission_required = 'view_question'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Question.objects.all().order_by('id'):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('question_create')
        context['title'] = 'Listado de Preguntas'
        return context


class QuestionCreateView(PermissionMixin, CreateView):
    model = Question
    template_name = 'question/create.html'
    form_class = QuestionForm
    success_url = reverse_lazy('question_list')
    permission_required = 'add_question'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Pregunta'
        context['action'] = 'add'
        return context


class QuestionUpdateView(PermissionMixin, UpdateView):
    model = Question
    template_name = 'question/create.html'
    form_class = QuestionForm
    success_url = reverse_lazy('question_list')
    permission_required = 'change_question'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Pregunta'
        context['action'] = 'edit'
        return context


class QuestionDeleteView(PermissionMixin, DeleteView):
    model = Question
    template_name = 'question/delete.html'
    success_url = reverse_lazy('question_list')
    permission_required = 'delete_question'

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
