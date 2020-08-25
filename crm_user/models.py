from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.utils import timezone

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
        
        user = self.model(
            email = self.normalize_email(email),
            login  = login,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,login,email,password):
        user = self.create_user(
            login = login,
            email = email,
            password = password
        )
        user.is_admin = True 
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=30,name='name')
    surname = models.CharField(max_length=30,name='surname')
    login = models.CharField(max_length=30,unique=True,null=True,name='login')
    password = models.TextField(null=True,name='password')
    email = models.CharField(max_length=40,unique=True,name='email')
    roleid = models.ForeignKey(UserRole,null=True,on_delete=models.CASCADE,name='roleid',related_name='users')
    dateofadd = models.DateTimeField(default = timezone.now)
    phone = models.CharField(max_length=20,null=True,blank=True,name='phone')
    is_admin = models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)
    
    USERNAME_FIELD = 'login' # this field will be used in auth part
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    def __str__(self):
        return self.login

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
