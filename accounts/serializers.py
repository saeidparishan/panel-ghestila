from rest_framework import serializers
from .models import User, Department


class UserSerializer(serializers.ModelSerializer):
    """
    اطلاعات کامل کاربر (برای نمایش)
    """
    department_name = serializers.CharField(source='department.department', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'role',
            'department',
            'department_name',
            'is_active',
            'is_verified',
            'is_staff',
        ]
        read_only_fields = ['is_staff', 'is_verified']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    ساخت کاربر جدید (ثبت‌نام)
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'role',
            'department',
            'password',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    تغییر رمز عبور کاربر
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        from django.contrib.auth.password_validation import validate_password
        validate_password(value)
        return value


