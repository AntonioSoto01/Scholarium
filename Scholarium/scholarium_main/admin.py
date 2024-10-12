from django.contrib import admin
from .models import Center, Group, Student, Teacher, CenterAdmin, SuperAdmin, Subject, Schedule, Attendance, Evaluation, Grade

admin.site.register(Center)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(CenterAdmin)
admin.site.register(SuperAdmin)
admin.site.register(Subject)
admin.site.register(Schedule)
admin.site.register(Attendance)
admin.site.register(Evaluation)
admin.site.register(Grade)