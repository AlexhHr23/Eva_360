import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from config import settings
from core.erp.forms import StudentForm, User, Student
from core.security.mixins import ModuleMixin, PermissionMixin


class StudentListView(PermissionMixin, TemplateView):
    template_name = 'student/list.html'
    permission_required = 'view_student'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Student.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('student_create')
        context['title'] = 'Listado de Estudiantes'
        return context


class StudentCreateView(PermissionMixin, CreateView):
    model = User
    template_name = 'student/create.html'
    form_class = StudentForm
    success_url = reverse_lazy('student_list')
    permission_required = 'add_student'

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
                    student = Student()
                    student.user_id = user.id
                    student.mobile = request.POST['mobile']
                    student.address = request.POST['address']
                    student.birthdate = request.POST['birthdate']
                    student.save()
                    group = Group.objects.get(pk=settings.GROUPS.get('student'))
                    user.groups.add(group)
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Student.objects.all()
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
        context['title'] = 'Nuevo registro de un Estudiante'
        context['action'] = 'add'
        return context


class StudentUpdateView(PermissionMixin, UpdateView):
    model = Student
    template_name = 'student/create.html'
    form_class = StudentForm
    success_url = reverse_lazy('student_list')
    permission_required = 'change_student'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = StudentForm(instance=instance.user, initial={
            'mobile': instance.mobile,
            'birthdate': instance.birthdate,
            'address': instance.address,
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
                    student = self.get_object()
                    student.mobile = request.POST['mobile']
                    student.address = request.POST['address']
                    student.birthdate = request.POST['birthdate']
                    student.save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Student.objects.all().exclude(id=self.get_object().id)
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
        context['title'] = 'Edición de un Estudiante'
        context['action'] = 'edit'
        return context


class StudentDeleteView(PermissionMixin, DeleteView):
    model = Student
    template_name = 'student/delete.html'
    success_url = reverse_lazy('student_list')
    permission_required = 'delete_student'

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


class StudentUpdateProfileView(ModuleMixin, UpdateView):
    model = User
    template_name = 'student/profile.html'
    form_class = StudentForm
    success_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = StudentForm(instance=instance, initial={
            'mobile': instance.student.mobile,
            'birthdate': instance.student.birthdate,
            'address': instance.student.address,
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

                    student = user.student
                    student.user_id = user.id
                    student.mobile = request.POST['mobile']
                    student.address = request.POST['address']
                    student.birthdate = request.POST['birthdate']
                    student.save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Student.objects.all().exclude(id=self.get_object().student.id)
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
