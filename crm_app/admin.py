from django.contrib import admin
from crm_app.models import Department,MealCategory,Meal,Table,Order,Check,ServicePercentage,Status
# Register your models here.
admin.site.register(Department)
admin.site.register(MealCategory)
admin.site.register(Meal)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(Check)
admin.site.register(ServicePercentage)
admin.site.register(Status)