from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from rest_framework import exceptions
# Create your models here.

class UserRole(models.Model):
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name

class MyUserManager(BaseUserManager):
    #! we have to have login and email since are required 
    def create_user(self,login,email,password):
        if not email:
            raise ValueError("email field is empty")
        
        if not login:
            raise ValueError("login field is empty")
        
        new_user = self.model(email = self.normalize_email(email),login  = login)

        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user
    
    def create_superuser(self,login,email,password):
        user = self.create_user(
            login = login,
            email = email,
            password = password
        )
        user.admin = True 
        user.staff = True
        user.superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=30,name='name')
    surname = models.CharField(max_length=30,name='surname')
    login = models.CharField(max_length=30,unique=True,null=True,name='login')
    email = models.CharField(max_length=40,unique=True,name='email')
    roleid = models.ForeignKey(UserRole,null=True,on_delete=models.CASCADE,name='roleid',related_name='users')
    dateofadd = models.DateTimeField(default = timezone.now)
    phone = models.CharField(max_length=20,null=True,blank=True,name='phone')
    admin = models.BooleanField(default=False)
    staff =  models.BooleanField(default=False)
    superuser =  models.BooleanField(default=False)
    active =  models.BooleanField(default=True)

    
    USERNAME_FIELD = 'login' # this field will be used in auth part
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

    # * @ property means that we can call function as regular property 
    # * ex : user.is_admin instead user.is_admin()
    @property 
    def is_admin(self):
        return self.admin
    
    @property 
    def is_superuser(self):
        return self.superuser

    @property 
    def is_active(self):
        return self.active
    
    @property 
    def is_staff(self):
        return self.staff