from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, CenterAdminViewSet, CenterViewSet, EvaluationViewSet, GradeViewSet, GroupViewSet, PersonUserViewSet, ScheduleViewSet, StudentViewSet, SubjectViewSet, SuperAdminViewSet, TeacherViewSet

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
router.register(r'user', PersonUserViewSet)

urlpatterns = [
    path('', include(router.urls)),

]