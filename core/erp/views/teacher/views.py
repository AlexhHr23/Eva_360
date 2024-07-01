import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from config import settings
from core.erp.forms import TeacherForm, User, Teacher
from core.security.mixins import ModuleMixin, PermissionMixin


class TeacherListView(PermissionMixin, TemplateView):
    template_name = 'teacher/list.html'
    permission_required = 'view_teacher'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Teacher.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('teacher_create')
        context['title'] = 'Listado de Profesores'
        return context


class TeacherCreateView(PermissionMixin, CreateView):
    model = User
    template_name = 'teacher/create.html'
    form_class = TeacherForm
    success_url = reverse_lazy('teacher_list')
    permission_required = 'add_teacher'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    user = User()
                    user.names = request.POST['names']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.create_or_update_password(user.dni)
                    user.email = request.POST['email']
                    user.save()
                    teacher = Teacher()
                    teacher.user_id = user.id
                    teacher.mobile = request.POST['mobile']
                    teacher.address = request.POST['address']
                    teacher.profession = request.POST['profession']
                    teacher.birthdate = request.POST['birthdate']
                    teacher.save()
                    group = Group.objects.get(pk=settings.GROUPS.get('teacher'))
                    user.groups.add(group)
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Teacher.objects.all()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Profesor'
        context['action'] = 'add'
        return context


class TeacherUpdateView(PermissionMixin, UpdateView):
    model = Teacher
    template_name = 'teacher/create.html'
    form_class = TeacherForm
    success_url = reverse_lazy('teacher_list')
    permission_required = 'change_teacher'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = TeacherForm(instance=instance.user, initial={
            'mobile': instance.mobile,
            'birthdate': instance.birthdate,
            'address': instance.address,
            'profession': instance.profession,
        })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    user = self.get_object().user
                    user.names = request.POST['names']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()
                    teacher = self.get_object()
                    teacher.mobile = request.POST['mobile']
                    teacher.address = request.POST['address']
                    teacher.profession = request.POST['profession']
                    teacher.birthdate = request.POST['birthdate']
                    teacher.save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Teacher.objects.all().exclude(id=self.get_object().id)
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Profesor'
        context['action'] = 'edit'
        return context


class TeacherDeleteView(PermissionMixin, DeleteView):
    model = Teacher
    template_name = 'teacher/delete.html'
    success_url = reverse_lazy('teacher_list')
    permission_required = 'delete_teacher'

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


class TeacherUpdateProfileView(ModuleMixin, UpdateView):
    model = User
    template_name = 'teacher/profile.html'
    form_class = TeacherForm
    success_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = TeacherForm(instance=instance, initial={
            'mobile': instance.teacher.mobile,
            'birthdate': instance.teacher.birthdate,
            'address': instance.teacher.address,
            'profession': instance.teacher.profession,
        })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    user = self.get_object()
                    user.names = request.POST['names']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    teacher = user.Teacher
                    teacher.user_id = user.id
                    teacher.mobile = request.POST['mobile']
                    teacher.address = request.POST['address']
                    teacher.profession = request.POST['profession']
                    teacher.birthdate = request.POST['birthdate']
                    teacher.save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Teacher.objects.all().exclude(id=self.get_object().teacher.id)
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de Perfil'
        context['action'] = 'edit'
        return context
