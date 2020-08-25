from django.db import models
from django.utils import timezone

# TODO fix Order model,problem with table_id and table_name

# ! Useful material
#  for the name of models use CapWords
#  for the name of attr snake_case
#  name models singular Role not Roles
#  related_name is for reverse relationship (we can access to User using Role objects)
#  Null is database related .
#  Blank is validation related . (form.is_valid() used here)

# Roles.roles.all() - Roles.objects.all()
# rename objects to roles using models.Manager()

class Department(models.Model):
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name

class MealCategory(models.Model):
    name = models.CharField(max_length=30,unique=True)
    department_id = models.ForeignKey(Department,on_delete=models.CASCADE,related_name='meal_categories')    

    def __str__(self):
        return self.name
        
class Meal(models.Model):
    name = models.CharField(max_length=30,unique=True)
    category_id = models.ForeignKey(MealCategory,on_delete=models.CASCADE,related_name='meals')
    price = models.IntegerField()
    # ! don't use null = True for text-based fields CharField and TextField
    # ! Two possible values for “no data,” that is: None and an empty string.
    description = models.TextField(blank=True) # * Optional
    amount = models.IntegerField(default=1,blank=True)
    total_price = models.IntegerField(null=True)

    def __str__(self):
        return self.name    

class Table(models.Model):
    name = models.CharField(max_length=10,unique=True)
    
    def __str__(self):
        return self.name



class Order(models.Model):
    waiter_id = models.IntegerField()
    table_id = models.ForeignKey(Table,on_delete=models.CASCADE,related_name = 'orders')
    table_name = models.CharField(max_length=10)
    isitopen = models.IntegerField()
    date = models.DateTimeField(default = timezone.now)
    meals = models.ForeignKey(Meal,on_delete=models.CASCADE,related_name='orders',null=True)

    def __str__(self):
        return self.table_name

class Check(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='checks')
    date = models.DateTimeField(default = timezone.now)
    servicefee = models.IntegerField()
    totalsum = models.IntegerField()
    meals = models.ForeignKey(Meal,on_delete=models.CASCADE,related_name='checks',null=True)

    def __str__(self):
        return self.order_id

class ServicePercentage(models.Model):
    percentage=models.IntegerField()

    def __str__(self):
        return self.percentage

class Status(models.Model):
    name = models.CharField(max_length=30,unique = True)
    def __str__(self):
        return self.name