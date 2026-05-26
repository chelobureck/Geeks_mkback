from rest_framework import serializers
from .models import Course, Group, Schedule, Grade
from apps.users.serializers import UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    teacher_details = UserSerializer(source='teacher', read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'teacher', 'teacher_details', 'students', 'course', 'schedules')

class GradeSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(source='student.email', read_only=True)
    
    class Meta:
        model = Grade
        fields = ('id', 'student', 'student_email', 'teacher', 'group', 'value', 'comment', 'date')
        read_only_fields = ('teacher', 'date')
