from django.contrib import admin

from .models import PlanTable,LeaveRequest,StatusDiscoverImage,WorkLog

# Register your models here.
admin.site.register(PlanTable)
admin.site.register(LeaveRequest)
admin.site.register(StatusDiscoverImage)
admin.site.register(WorkLog)
