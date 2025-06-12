from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# from .departments import Department


class CustomUserManager(BaseUserManager): #یک کلاس CustomUserManager هست که وظیفه‌ی مدیریت ساخت کاربران (معمولی و ادمین) در سیستم احراز هویت Django رو داره
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("لطفا username را وارد کنید")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'مدیر سیستم'),
        ('manager', 'مدیریت'),
        ('human_resources', 'مدیر منابع انسانی'),
        ('department_manager', 'مدیر بخش'),
        ('supervisor', 'سرپرست'),
        ('employee', 'کارمند'),
    )
    
    username = models.CharField(max_length=45,unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='employee')
    department = models.ForeignKey(
        'accounts.Department',  # استفاده از رشته برای جلوگیری از circular import
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.username})"
    
    
    

class Department(models.Model):
    DEPARTMENT_CHOICES = (
        ('admin', 'مدیر سیستم'),
        ('manager', 'مدیریت'),
        ('site', 'سایت'),
        ('it', 'آی تی'),
        ('human_resources', 'منابع انسانی'),
        ('finance', 'مالی'),
        ('support', 'پشتیبانی'),
        ('sales', 'فروش'),
        ('adminstrative', 'اداری'),
        ('formal', 'حضوری'),
        ('content', 'محتوا'),
    )
    department = models.CharField(max_length=35, choices=DEPARTMENT_CHOICES)
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name="supervisor_departments")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True, related_name="managed_departments")

    def __str__(self):
        return self.department
    