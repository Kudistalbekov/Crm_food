from django.contrib import admin
from crm_user.models import UserRole,MyUser
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoAdmin
from .forms import UserChangeForm
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(DjangoAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('login',)
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','surname','login','roleid','dateofadd','phone',)}),
        ('Permissions', {'fields': ('admin','staff','superuser','active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','login',)
    ordering = ('login',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)

admin.site.unregister(Group)
admin.site.register(UserRole)

