from config.wsgi import *
import string
import random

from core.erp.models import *
from core.security.models import *
from django.contrib.auth.models import Permission
from core.user.models import User

numbers = list(string.digits)

dashboard = Dashboard()
dashboard.name = 'Evaluación360'
dashboard.icon = 'fa-solid fa-cube'
dashboard.layout = 1
dashboard.navbar = 'navbar-dark navbar-primary'
dashboard.sidebar = 'sidebar-dark-primary'
dashboard.save()

moduletype = ModuleType()
moduletype.name = 'Seguridad'
moduletype.icon = 'fas fa-lock'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 1
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.save()
for i in Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Conf. Dashboard'
module.url = '/security/dashboard/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.save()
for i in Permission.objects.filter(content_type__model=AccessUsers._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Usuarios'
module.url = '/user/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar a los usuarios del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Gestión Académica'
moduletype.icon = 'fa-solid fa-graduation-cap'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 2
module.name = 'Estudiantes'
module.url = '/erp/student/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-user-group'
module.description = 'Permite administrar a los estudiantes del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Student._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Profesores'
module.url = '/erp/teacher/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-person-chalkboard'
module.description = 'Permite administrar a los profesores del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Teacher._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Encuentas'
moduletype.icon = 'fa-solid fa-clipboard-list'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 3
module.name = 'Categorías'
module.url = '/erp/category/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-table-list'
module.description = 'Permite administrar las categorias de las preguntas'
module.save()
for i in Permission.objects.filter(content_type__model=Category._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Preguntas'
module.url = '/erp/question/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-clipboard-question'
module.description = 'Permite administrar las preguntas de las encuentas'
module.save()
for i in Permission.objects.filter(content_type__model=Question._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Registro de Encuestas'
module.url = '/erp/quiz/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fa-solid fa-folder-open'
module.description = 'Permite administrar las encuentas del sistema'
module.save()
module.permits.add(Permission.objects.get(codename='view_quiz'))
module.permits.add(Permission.objects.get(codename='add_quiz'))
module.permits.add(Permission.objects.get(codename='change_quiz'))
module.permits.add(Permission.objects.get(codename='delete_quiz'))
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Reportes'
moduletype.icon = 'fas fa-chart-pie'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 4
module.name = 'Encuestas'
module.url = '/reports/quiz/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las encuestas'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Cambiar password'
module.url = '/user/update/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Editar perfil'
module.url = '/user/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Editar perfil'
module.url = '/erp/student/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite editar el perfil del estudiante'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Editar perfil'
module.url = '/erp/teacher/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite editar el perfil del profesor'
module.save()
print(f'insertado {module.name}')

group = Group()
group.name = 'Administrador'
group.save()
print(f'insertado {group.name}')

for m in Module.objects.filter().exclude(url__in=['/erp/student/update/profile/', '/erp/teacher/update/profile/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for p in m.permits.all():
        group.permissions.add(p)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = p.id
        grouppermission.save()

module = Module()
module.name = 'Encuestas'
module.url = '/erp/quiz/user/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fa-solid fa-folder-open'
module.description = 'Permite administrar las respuestas de las encuentas del sistema'
module.save()
module.permits.add(Permission.objects.get(codename='view_quiz_user'))
print(f'insertado {module.name}')

group = Group()
group.name = 'Estudiante'
group.save()
print(f'insertado {group.name}')

for m in Module.objects.filter(url__in=['/erp/student/update/profile/', '/user/update/password/', '/erp/quiz/user/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()

group = Group()
group.name = 'Profesor'
group.save()
print(f'insertado {group.name}')

for m in Module.objects.filter(url__in=['/erp/teacher/update/profile/', '/user/update/password/', '/erp/quiz/user/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()

user = User()
user.names = 'William Jair Dávila Vargas'
user.username = 'admin'
user.dni = ''.join(random.choices(numbers, k=10))
user.email = 'davilawilliam93@gmail.com'
user.is_active = True
user.is_superuser = True
user.is_staff = True
user.set_password('hacker94')
user.save()
user.groups.add(Group.objects.first())
print(f'Bienvenido {user.names}')
