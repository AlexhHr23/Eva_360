import os
import uuid

from crum import get_current_request
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

from config import settings


class User(AbstractBaseUser, PermissionsMixin):
    names = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nombres')
    username = models.CharField(max_length=150, unique=True, verbose_name='Username')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Número de cedula')
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    email = models.EmailField(null=True, blank=True, verbose_name='Correo electrónico')
    is_active = models.BooleanField(default=True, verbose_name='Estado')
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_change_password = models.BooleanField(default=False)
    email_reset_token = models.TextField(null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def toJSON(self):
        item = model_to_dict(self, exclude=['last_login', 'email_reset_token', 'password', 'user_permissions'])
        item['image'] = self.get_image()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['groups'] = [{'id': i.id, 'name': i.name} for i in self.groups.all()]
        item['last_login'] = None if self.last_login is None else self.last_login.strftime('%Y-%m-%d')
        return item

    def get_full_name(self):
        return f'{self.names} ({self.dni})'

    def generate_token(self):
        return str(uuid.uuid4())

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def remove_image(self):
        try:
            if self.image:
                os.remove(self.image.path)
        except:
            pass
        finally:
            self.image = None

    def delete(self, using=None, keep_parents=False):
        self.remove_image()
        super(User, self).delete()

    def get_group_id_session(self):
        try:
            request = get_current_request()
            return int(request.session['group'].id)
        except:
            return 0

    def set_group_session(self):
        try:
            request = get_current_request()
            groups = request.user.groups.all()
            if groups:
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass

    def create_or_update_password(self, password):
        if self.pk is None:
            self.set_password(password)
        else:
            user = User.objects.get(pk=self.pk)
            if user.password != password:
                self.set_password(password)

    def get_short_name(self):
        if self.names is not None:
            names = self.names.split(' ')
            if len(names) > 1:
                return f'{names[0]} {names[1]}'
        return self.names

    def is_student(self):
        return hasattr(self, 'student')

    def __str__(self):
        return self.names

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-id']
