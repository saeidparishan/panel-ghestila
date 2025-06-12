from rest_framework import serializers

from.models import PlanTable, LeaveRequest, StatusDiscoverImage, WorkLog

# برای PlanTable
class PlanTableSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = PlanTable
        fields = ['id', 'department', 'department_name', 'day', 'description']
        read_only_fields = ['department_name', 'department']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['department'] = request.user.department
        return super().create(validated_data)


# برای LeaveRequest
class LeaveRequestSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'user', 'user_full_name',
            'start_day', 'end_day', 'description',
            'status', 'status_display', 'created_at'
        ]
        read_only_fields = ['user', 'created_at', 'status', 'user_full_name', 'status_display']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        role = user.role
        status = 'pending_1'
        if role == 'supervisor':
            status = 'pending_2'
        elif role == 'department_manager':
            status = 'pending_3'
        elif role == 'human_resources':
            status = 'pending_4'
        validated_data['status'] = status
        return super().create(validated_data)


# برای تصاویر وضعیت درخواست
class StatusDiscoverImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(source='image', read_only=True)

    class Meta:
        model = StatusDiscoverImage
        fields = ['id', 'status', 'image_url']


# برای WorkLog
class WorkLogSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = WorkLog
        fields = [
            'id', 'user', 'user_full_name',
            'start_time', 'end_time', 'report', 'date'
        ]
        read_only_fields = ['user', 'date', 'user_full_name']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
