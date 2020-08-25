from django.contrib import admin
from crm_user.models import MyUser,UserRole
# Register your models here.

admin.site.register(MyUser)
admin.site.register(UserRole)

