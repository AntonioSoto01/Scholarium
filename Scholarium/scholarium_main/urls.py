from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CenterViewSet, GroupViewSet, StudentViewSet, TeacherViewSet, CenterAdminViewSet, SuperAdminViewSet, SubjectViewSet, ScheduleViewSet, AttendanceViewSet, EvaluationViewSet, GradeViewSet

router = DefaultRouter()
router.register(r'centers', CenterViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'center-admins', CenterAdminViewSet)
router.register(r'super-admins', SuperAdminViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'attendances', AttendanceViewSet)
router.register(r'evaluations', EvaluationViewSet)
router.register(r'grades', GradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]