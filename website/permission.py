from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
  
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
    
    
class LeaveRequestPermission(permissions.BasePermission):
    
    massage =  "شما اجازه انجام این عملیات را ندارید"
    
    def has_permission(self, request, view):
        if request.method == 'POST' and view.action == 'create':
            return request.user.role in ['employee', 'supervisor', 'department_manager']
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        # فقط مشاهده (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            if user.role in ['manager', 'human_resources']:
                return True
            if user.role in ['department_manager', 'supervisor']:
                return obj.user.department == user.department
            return obj.user == user

        # جلوگیری از حذف و ویرایش
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return False

        # اگر در حال تایید/رد باشد
        if view.action in ['approve', 'reject']:
            if user.role in ['human_resources', 'manager']:
                return True
            if user.role in ['supervisor', 'department_manager']:
                return obj.user.department == user.department
        return False

class IsDepartmentManagerOrReadOnly(permissions.BasePermission):
 
    message = "شما دسترسی لازم را ندارید."
    
    def has_permission(self, request, view):
        # متدهای امن مثل GET, HEAD, OPTIONS برای همه مجازه
        if request.method in permissions.SAFE_METHODS:
            return True

        # فقط مدیر دپارتمان اجازه ایجاد داره ولی بررسی دقیق‌تر روی آبجکت در has_object_permission انجام میشه
        return request.user.role == 'department_manager'

    def has_object_permission(self, request, view, obj):
        # متدهای امن مثل GET برای همه آزاد
        if request.method in permissions.SAFE_METHODS:
            return True

        # فقط اگر مدیر دپارتمان باشه و آبجکت متعلق به دپارتمان خودش باشه
        return request.user.role == 'department_manager' and obj.department == request.user.department




class WorkLogPermission(permissions.BasePermission):
    
    message = "شما دسترسی لازم را ندارید." 
    
    def has_permission(self, request, view):
        # فقط employee و supervisor اجازه POST دارند
        if request.method == 'POST':
            return request.user.role in ['employee', 'supervisor']

        # برای سایر متدها فقط احراز هویت بررسی شود
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # فقط مشاهده (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            if user.role == 'manager':
                return True
            if user.role == 'department_manager' and obj.user.department == user.department:
                return True
            return obj.user == user

        # هیچ‌کس اجازه ویرایش یا حذف ندارد
        return False
