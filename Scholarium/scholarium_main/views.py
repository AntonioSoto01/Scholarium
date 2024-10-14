from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Attendance, Center, CenterAdmin, Evaluation, Grade, Group, PersonUser, Schedule, Student, Subject, SuperAdmin, Teacher
from .serializers import AttendanceSerializer, CenterAdminSerializer, CenterSerializer, EvaluationSerializer, GradeSerializer, GroupSerializer, PersonUserSerializer, ScheduleSerializer, StudentSerializer, SubjectSerializer, SuperAdminSerializer, TeacherSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
class CenterViewSet(viewsets.ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializer
    permission_classes = [IsAuthenticated]

    def get_person(self):
        return getattr(self.request.user, 'person', None)

    def get_queryset(self):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            return Center.objects.all()
        elif isinstance(person, Student):
            return Center.objects.filter(id=person.group.center.id)
        return Center.objects.filter(id=self.request.user.person.center_id)

    def perform_create(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
            redirect_url = "https://www.ejemplo.com"
            return Response({'redirect_url': redirect_url}, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied("No tienes permiso para crear un nuevo centro.")

    def perform_update(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
        elif isinstance(person, CenterAdmin) and self.request.user.person.center_id == serializer.instance.id:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar este centro.")

    def perform_destroy(self, instance):
        if isinstance(self.get_person(), SuperAdmin):
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar este centro.")


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_person(self):
        return getattr(self.request.user, 'person', None)

    def get_queryset(self):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            return Student.objects.all()
        elif isinstance(person, CenterAdmin):
            return Student.objects.filter(center=person.center)
        elif isinstance(person, Student):
            return Student.objects.filter(group=person.group)
        elif isinstance(person, Teacher):
            return Student.objects.filter(group__in=person.schedule_set.values_list('group', flat=True)).distinct()
        return Student.objects.none()


    def perform_create(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            student = serializer.save()
            response = HttpResponseRedirect('https://www.example.com')
            response.status_code = status.HTTP_303_SEE_OTHER
            return response
        else:
            raise PermissionDenied("No tienes permiso para crear un nuevo alumno.")

    def perform_update(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
        elif isinstance(person, Student) and person.id == serializer.instance.id:
            serializer.save()
        elif isinstance(person, CenterAdmin):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar este alumno.")

    def perform_destroy(self, instance):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar este alumno.")

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_person(self):
        return getattr(self.request.user, 'person', None)

    def get_queryset(self):
        person = self.get_person()
        
        if isinstance(person, SuperAdmin):
            return Teacher.objects.all()
        
        if isinstance(person, CenterAdmin):
            return Teacher.objects.filter(center=person.center)

        if isinstance(person, Teacher):
            return Teacher.objects.filter(id=person.id)
        
        if isinstance(person, Student):
            return Teacher.objects.filter(schedule__group=person.group).distinct()
        
        return Teacher.objects.none()

    def perform_create(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para crear un nuevo profesor.")

    def perform_update(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin) or (isinstance(person, Teacher) and person == serializer.instance):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar este profesor.")

    def perform_destroy(self, instance):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar este profesor.")


class CenterAdminViewSet(viewsets.ModelViewSet):
    queryset = CenterAdmin.objects.all()
    serializer_class = CenterAdminSerializer
    permission_classes = [IsAuthenticated]

    def get_person(self):
        return getattr(self.request.user, 'person', None)

    def get_queryset(self):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            return CenterAdmin.objects.all()
        elif isinstance(person, Student):
            return CenterAdmin.objects.filter(center=person.group.center)     
        return CenterAdmin.objects.filter(center=person.center)

    def perform_create(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para crear un nuevo administrador de centro.")

    def perform_update(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
        if isinstance(person, CenterAdmin) and person == serializer.instance:
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar este administrador de centro.")

    def perform_destroy(self, instance):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar este administrador de centro.")


class SuperAdminViewSet(viewsets.ModelViewSet):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer
    permission_classes = [IsAuthenticated]

    def get_person(self):
        return getattr(self.request.user, 'person', None)

    def get_queryset(self):
        return SuperAdmin.objects.all()

    def perform_create(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para crear un superadministrador.")

    def perform_update(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar un superadministrador.")

    def perform_destroy(self, instance):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar un superadministrador.")



class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_person(self):
        return getattr(self.request.user, 'person', None)

    def get_queryset(self):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            return Subject.objects.all()
        elif isinstance(person, CenterAdmin):
            return Subject.objects.filter(schedule__group__center=person.center).distinct()
        elif isinstance(person, Teacher):
            return Subject.objects.filter(schedule__teacher=person).distinct()
        elif isinstance(person, Student):
            return Subject.objects.filter(schedule__group=person.group).distinct()
        return Subject.objects.none()

    def perform_create(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para crear una asignatura.")

    def perform_update(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar esta asignatura.")

    def perform_destroy(self, instance):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar esta asignatura.")


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_person(self):
        return getattr(self.request.user, 'person', None)

    def get_queryset(self):
        person = self.get_person()
        if isinstance(person, SuperAdmin):
            return Schedule.objects.all()
        elif isinstance(person, CenterAdmin):
            return Schedule.objects.filter(group__center=person.center)
        elif isinstance(person, Teacher):
            return Schedule.objects.filter(teacher=person) | Schedule.objects.filter(group__teacher=person)
        elif isinstance(person, Student):
            return Schedule.objects.filter(group=person.group)
        return Schedule.objects.none()

    def perform_create(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin) or (isinstance(person, CenterAdmin) and serializer.validated_data['group'].center == person.center):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para crear un horario.")

    def perform_update(self, serializer):
        person = self.get_person()
        if isinstance(person, SuperAdmin) or (isinstance(person, CenterAdmin) and serializer.instance.group.center == person.center):
            serializer.save()
        else:
            raise PermissionDenied("No tienes permiso para editar este horario.")

    def perform_destroy(self, instance):
        person = self.get_person()
        if isinstance(person, SuperAdmin) or (isinstance(person, CenterAdmin) and instance.group.center == person.center):
            instance.delete()
        else:
            raise PermissionDenied("No tienes permiso para eliminar este horario.")


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
class PersonUserViewSet(viewsets.ModelViewSet):
    queryset = PersonUser.objects.all()
    serializer_class = PersonUserSerializer
    permission_classes = [IsAuthenticated]
    def get_person(self):
        return getattr(self.request.user, 'person', None)

    def perform_create(self, serializer):
        person= self.get_person()
        if isinstance(person, SuperAdmin) or self.request.user.is_superuser:
            serializer.save()
