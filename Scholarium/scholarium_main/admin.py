from django.contrib import admin
from .models import Center, Group, PersonUser, Student, Teacher, CenterAdmin, SuperAdmin, Subject, Schedule, Attendance, Evaluation, Grade
from django.contrib.auth.admin import UserAdmin
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
@admin.register(PersonUser)
class PersonUserAdmin(admin.ModelAdmin):
    exclude = ['content_type', 'object_id','first_name', 'last_name'] 
    readonly_fields = ['person']