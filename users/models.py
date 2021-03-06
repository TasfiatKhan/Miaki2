from django.db import models
from django.conf import settings 
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must provide an email')
        if not username:
            raise ValueError('User must provide an username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email), 
            username=username, 
            password=password,
            )
        user.is_admin = True
        user.is_superuser = True
        user.save()
        
        return user        
        
        

class User(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=60, null=True, unique=True)
    
    date_joined = models.DateTimeField(verbose_name='date joined', null=True, auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', null=True, auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perm(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin