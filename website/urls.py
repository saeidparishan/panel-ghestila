from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    PlanTableViewSet,
    LeaveRequestViewSet,
    StatusDiscoverImageViewSet,
    WorkLogViewSet,
)

router = DefaultRouter()
router.register(r'plan-tables', PlanTableViewSet, basename='plan-table') 
router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')
router.register(r'status-images', StatusDiscoverImageViewSet, basename='status-image')
router.register(r'work-logs', WorkLogViewSet, basename='work-log')

urlpatterns = [
    path('api/', include(router.urls)),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
