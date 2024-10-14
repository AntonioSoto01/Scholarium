from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class Center(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Group(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    school_year = models.CharField(max_length=9) 
    course_number = models.CharField(max_length=10)
    letter = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.school_year} - {self.course_number}{self.letter} - {self.center}"

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Student(Person):
    enrollment_number = models.CharField(max_length=20, unique=True)
    # course = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Teacher(Person):
    employee_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)

class CenterAdmin(Person):
    employee_number = models.CharField(max_length=20, unique=True)
    office = models.CharField(max_length=50)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)

class SuperAdmin(Person):
    employee_number = models.CharField(max_length=20, unique=True)
    special_permissions = models.TextField()

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.subject.name} - {self.day_of_week} {self.start_time}-{self.end_time}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {'Presente' if self.present else 'Ausente'}"

class Evaluation(models.Model):
    EVALUATION_CHOICES = [
        ('Inicial', 'Inicial'),
        ('Primera', 'Primera'),
        ('Segunda', 'Segunda'),
        ('Tercera', 'Tercera'),
    ]
    name = models.CharField(max_length=100, choices=EVALUATION_CHOICES)
    date = models.DateField()

    def __str__(self):
        return self.name

class Grade(models.Model):
    GRADE_CHOICES = [
        ('Insuficiente', 'Insuficiente'),
        ('Suficiente', 'Suficiente'),
        ('Bien', 'Bien'),
        ('Notable', 'Notable'),
        ('Sobresaliente', 'Sobresaliente'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)

    def __str__(self):
        return f"{self.student} - {self.subject.name} - {self.evaluation.name} - {self.grade}"
    
#Workaround for the foreign key for abstract class problem 
class PersonUser(AbstractUser):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    person = GenericForeignKey('content_type', 'object_id')
    def __str__(self):
        return self.username