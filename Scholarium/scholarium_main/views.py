from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Center, Group, Student, Teacher, CenterAdmin, SuperAdmin, Subject, Schedule, Attendance, Evaluation, Grade
from .serializers import CenterSerializer, GroupSerializer, StudentSerializer, TeacherSerializer, CenterAdminSerializer, SuperAdminSerializer, SubjectSerializer, ScheduleSerializer, AttendanceSerializer, EvaluationSerializer, GradeSerializer
from .permissions import IsSuperAdmin, IsCenterAdmin, IsTeacher, IsStudent, IsCenterMember, IsTeacherOrReadOnly, IsStudentOrReadOnly

class CenterViewSet(viewsets.ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin | IsCenterMember]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin | IsCenterAdmin | IsTeacher]

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin | IsCenterAdmin | IsTeacher | IsStudentOrReadOnly]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin | IsCenterAdmin]

class CenterAdminViewSet(viewsets.ModelViewSet):
    queryset = CenterAdmin.objects.all()
    serializer_class = CenterAdminSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class SuperAdminViewSet(viewsets.ModelViewSet):
    queryset = SuperAdmin.objects.all()
    serializer_class = SuperAdminSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin | IsCenterAdmin | IsTeacher]

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated, IsCenterAdmin | IsTeacher]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrReadOnly]