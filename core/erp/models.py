import json
import uuid
from datetime import datetime

from django.db import models

from core.erp.choices import TYPE_QUIZ, STATUS_QUIZ_ANSWERS
from core.user.models import User
from django.forms import model_to_dict


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    def delete(self, using=None, keep_parents=False):
        super(Student, self).delete()
        try:
            self.user.delete()
        except:
            pass

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['-id']


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=50, verbose_name='Profesión')
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    def delete(self, using=None, keep_parents=False):
        super(Teacher, self).delete()
        try:
            self.user.delete()
        except:
            pass

    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-id']


class Question(models.Model):
    description = models.CharField(max_length=500, verbose_name='Descripción')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    state = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.description} ({self.category.name})'

    def toJSON(self):
        item = model_to_dict(self)
        item['category'] = self.category.toJSON()
        return item

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['-id']


class Quiz(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    instructions = models.CharField(max_length=2000, verbose_name='Instrucciones')
    type = models.CharField(max_length=20, choices=TYPE_QUIZ, default=TYPE_QUIZ[0][0], verbose_name='Tipo de Encuesta')
    access_key = models.CharField(max_length=200, verbose_name='Clave de acceso')
    state = models.BooleanField(default=False, verbose_name='Estado')

    def __str__(self):
        return self.name

    def activate_quiz(self):
        if self.type == TYPE_QUIZ[0][0]:
            users = Student.objects.all()
        else:
            users = Teacher.objects.all()
        for i in users:
            quiz_answers = QuizAnswers()
            quiz_answers.quiz_id = self.id
            quiz_answers.user = i.user
            quiz_answers.save()
            for d in self.quizdetail_set.all():
                detail = QuizAnswersDetail()
                detail.quiz_answers_id = quiz_answers.id
                detail.quiz_detail_id = d.id
                detail.answer = -1
                detail.save()

    def toJSON(self):
        item = model_to_dict(self)
        item['number'] = f'{self.id:06d}'
        item['type'] = {'id': self.type, 'name': self.get_type_display()}
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.access_key = str(uuid.uuid4())[0:50]
        super(Quiz, self).save()

    class Meta:
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'
        default_permissions = ()
        permissions = (
            ('view_quiz', 'Can view Encuesta'),
            ('add_quiz', 'Can add Encuesta'),
            ('change_quiz', 'Can change Encuesta'),
            ('delete_quiz', 'Can delete Encuesta'),
            ('view_quiz_user', 'Can view Encuesta | User'),
            ('add_quiz_user', 'Can add Encuesta | User'),
        )
        ordering = ['-id']


class QuizDetail(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

    def __str__(self):
        return self.question.description

    def toJSON(self):
        item = model_to_dict(self, exclude=['quiz'])
        item['question'] = self.question.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle de Encuesta'
        verbose_name_plural = 'Detalle de Encuestas'
        default_permissions = ()
        ordering = ['-id']


class QuizAnswers(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STATUS_QUIZ_ANSWERS, default=STATUS_QUIZ_ANSWERS[0][0])

    def __str__(self):
        return self.quiz.name

    def get_questions(self):
        data = []
        for i in self.quizanswersdetail_set.all():
            data.append(i.toJSON())
        return json.dumps(data)

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['status'] = {'id': self.status, 'name': self.get_status_display()}
        item['quiz'] = self.quiz.toJSON()
        item['user'] = self.user.toJSON()
        return item

    class Meta:
        verbose_name = 'Respuesta del cuestionario'
        verbose_name_plural = 'Respuestas del cuestionario'
        default_permissions = ()
        ordering = ['-id']


class QuizAnswersDetail(models.Model):
    quiz_answers = models.ForeignKey(QuizAnswers, on_delete=models.CASCADE)
    quiz_detail = models.ForeignKey(QuizDetail, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.IntegerField(default=-1)

    def __str__(self):
        return self.quiz_answers.quiz.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['quiz_answers'])
        item['quiz_detail'] = self.quiz_detail.toJSON()
        return item

    class Meta:
        verbose_name = 'Detalle de Respuesta del cuestionario'
        verbose_name_plural = 'Detalle de Respuestas del cuestionario'
        default_permissions = ()
        ordering = ['-id']
