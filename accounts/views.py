from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from accounts.models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    ChangePasswordSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API برای مدیریت کاربران.
    - ثبت‌نام
    - نمایش اطلاعات کاربر جاری
    - تغییر رمز عبور
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id != request.user.id:
            return Response(
                {"detail": "شما اجازه دسترسی به این اطلاعات را ندارید."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        raise PermissionDenied("ویرایش اطلاعات مجاز نیست.")

    def partial_update(self, request, *args, **kwargs):
        raise PermissionDenied("ویرایش اطلاعات مجاز نیست.")

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("حذف کاربر مجاز نیست.")

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not user.check_password(old_password):
            return Response(
                {"detail": "رمز فعلی اشتباه است."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response({"detail": "رمز عبور با موفقیت تغییر کرد."}, status=status.HTTP_200_OK)

