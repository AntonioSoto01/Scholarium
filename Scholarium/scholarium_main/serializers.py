from rest_framework import serializers

from  django.apps import apps
from .models import Center, Group, Person, PersonUser, Student, Teacher, CenterAdmin, SuperAdmin, Subject, Schedule, Attendance, Evaluation, Grade
from django.contrib.contenttypes.models import ContentType

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class CenterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CenterAdmin
        fields = '__all__'

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class PersonUserSerializer(serializers.ModelSerializer):
    person_id = serializers.IntegerField(write_only=True)
    person = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PersonUser
        fields = ('username', 'email', 'password', 'person_id', 'person')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        person_id = validated_data.pop('person_id')

        # Buscar en todas las subclases de Person
        person_instance = None
        for model in apps.get_models():
            if issubclass(model, Person) and model is not Person:
                try:
                    person_instance = model.objects.get(id=person_id)
                    break
                except model.DoesNotExist:
                    continue

        if person_instance is None:
            raise serializers.ValidationError('Person with the given ID does not exist.')

        content_type = ContentType.objects.get_for_model(person_instance)
        if PersonUser.objects.filter(content_type=content_type, object_id=person_instance.id).exists():
            raise serializers.ValidationError('A user account is already associated with this person.')

        object_id = person_instance.id

        user = PersonUser(**validated_data)
        user.set_password(password)
        user.content_type = content_type
        user.object_id = object_id
        user.save()
        return user

    def get_person(self, obj):
        if obj.content_type and obj.object_id:
            person_instance = obj.content_type.get_object_for_this_type(id=obj.object_id)
            return {
                'id': person_instance.id,
                'type': obj.content_type.model,
            }
        return None