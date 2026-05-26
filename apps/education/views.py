from rest_framework import viewsets, permissions
from .models import Course, Group, Schedule, Grade
from .serializers import CourseSerializer, GroupSerializer, ScheduleSerializer, GradeSerializer
from .permissions import IsCurator, IsTeacher, IsStudent, IsTeacherOrCurator

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCurator()]
        return [permissions.IsAuthenticated()]

class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CURATOR':
            return Group.objects.all()
        elif user.role == 'TEACHER':
            return Group.objects.filter(teacher=user)
        elif user.role == 'STUDENT':
            return Group.objects.filter(students=user)
        return Group.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsCurator()]
        if self.action in ['update', 'partial_update']:
            return [IsTeacherOrCurator()]
        return [permissions.IsAuthenticated()]

class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CURATOR':
            return Schedule.objects.all()
        return Schedule.objects.filter(group__in=user.enrolled_groups.all() | user.teaching_groups.all())

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCurator()]
        return [permissions.IsAuthenticated()]

class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'CURATOR':
            return Grade.objects.all()
        elif user.role == 'TEACHER':
            return Grade.objects.filter(teacher=user)
        elif user.role == 'STUDENT':
            return Grade.objects.filter(student=user)
        return Grade.objects.none()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsTeacherOrCurator()]
        return [permissions.IsAuthenticated()]
