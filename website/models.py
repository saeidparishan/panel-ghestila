from django.db import models
import django_jalali.db.models as jmodels

from accounts.models import Department,User
# Create your models here.
class PlanTable(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="calendar_entries")
    day = models.CharField(max_length=30,verbose_name="روز")
    description = models.TextField()
    
    def __str__(self):
        return self.day
    
class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending_1', 'منتظر تایید سرپرست'),
        ('approved_1', 'تایید توسط سرپرست'),
        ('rejected_1', 'رد توسط سرپرست'),
        ('pending_2', 'منتظر تایید مدیر بخش'),
        ('approved_2', 'تایید توسط مدیر بخش'),
        ('rejected_2', 'رد توسط مدیر بخش'),
        ('pending_3', 'منتظر تایید مدیر منابع انسانی'),
        ('approved_3', 'تایید توسط مدیر منابع انسانی'),
        ('rejected_3', 'رد توسط مدیر منابع انسانی'),
        ('pending_4', 'منتظر تایید مدیر'),
        ('approved_4', 'تایید نهایی'),
        ('rejected_4', 'رد نهایی'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_requester')
    start_day = jmodels.jDateField()
    end_day = jmodels.jDateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_1')
    created_at = jmodels.jDateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f'درخواست مرخصی {self.user.full_name}'
    
class StatusDiscoverImage(models.Model):
    status = models.CharField(max_length=30)
    image = models.ImageField()

    def __str__(self):
        return self.status

class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_logs')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    report = models.TextField(null=True, blank=True)
    date = jmodels.jDateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.date}"
    
    
    
    
