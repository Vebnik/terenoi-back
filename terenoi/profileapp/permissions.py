from rest_framework import permissions


class IsStudent(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.role == 'ST':
            return True


class IsTeacher(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.role == 'TH':
            return True
