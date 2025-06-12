from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import PlanTable, LeaveRequest, StatusDiscoverImage, WorkLog
from .serializers import (
    PlanTableSerializer,
    LeaveRequestSerializer,
    StatusDiscoverImageSerializer,
    WorkLogSerializer
)

from accounts.models import User
from website.utils import STATUS_VISIBILITY
from .permission import IsDepartmentManagerOrReadOnly, WorkLogPermission,  LeaveRequestPermission
# # Custom Permissions
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'manager'

class IsDepartmentManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'department_manager'

class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'supervisor'

class IsHR(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'human_resources'

class PlanTableViewSet(viewsets.ModelViewSet):
    serializer_class = PlanTableSerializer
    permission_classes = [permissions.IsAuthenticated, IsDepartmentManagerOrReadOnly] 

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return PlanTable.objects.all()
        elif user.role in ['department_manager', 'supervisor']:
            return PlanTable.objects.filter(department=user.department)
        return PlanTable.objects.filter(department=user.department)

    def perform_create(self, serializer):
        serializer.save(department=self.request.user.department)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated, LeaveRequestPermission]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'employee':
            return LeaveRequest.objects.filter(user=user)

        visible_requests = LeaveRequest.objects.none()
        for status, roles in STATUS_VISIBILITY.items():
            if user.role in roles:
                requests_for_status = LeaveRequest.objects.filter(
                    status=status, user__department=user.department
                )
                visible_requests = visible_requests | requests_for_status

        if user.role == 'human_resources':
            return LeaveRequest.objects.all()
        if user.role == 'manager':
            visible_requests |= LeaveRequest.objects.filter(status__in=['pending_4', 'approved_4'])

        return visible_requests.distinct()

    def perform_create(self, serializer):
        role = self.request.user.role
        status_map = {
            'employee': 'pending_1',
            'supervisor': 'pending_2',
            'department_manager': 'pending_3',
            'human_resources': 'pending_4',
        }
        serializer.save(user=self.request.user, status=status_map.get(role, 'pending_1'))

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        return self._update_status(request, pk, approve=True)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        return self._update_status(request, pk, approve=False)

    def _update_status(self, request, pk, approve=True):
        instance = get_object_or_404(LeaveRequest, pk=pk)
        role = request.user.role

        next_status = {
            'supervisor': 'pending_2' if approve else 'rejected_1',
            'department_manager': 'pending_3' if approve else 'rejected_2',
            'human_resources': 'pending_4' if approve else 'rejected_3',
            'manager': 'approved_4' if approve else 'rejected_4',
        }

        if role not in next_status:
            return Response({'detail': 'شما اجازه تغییر وضعیت ندارید.'}, status=status.HTTP_403_FORBIDDEN)

        # HR/Manager can view all, others only their own department
        if role not in ['human_resources', 'manager'] and instance.user.department != request.user.department:
            return Response({'detail': 'شما به این درخواست دسترسی ندارید.'}, status=status.HTTP_403_FORBIDDEN)

        instance.status = next_status[role]
        instance.save()
        return Response({'detail': 'وضعیت درخواست بروزرسانی شد.'})


class StatusDiscoverImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StatusDiscoverImage.objects.all()
    serializer_class = StatusDiscoverImageSerializer
    permission_classes = [permissions.IsAuthenticated]



class WorkLogViewSet(viewsets.ModelViewSet):
    serializer_class = WorkLogSerializer
    permission_classes = [permissions.IsAuthenticated, WorkLogPermission]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return WorkLog.objects.all()
        if user.role == 'department_manager':
            return WorkLog.objects.filter(user__department=user.department)
        return WorkLog.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



