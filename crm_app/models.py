from django.db import models
from django.utils import timezone

# TODO fix Order model,problem with table_id and table_name

# ! Useful material
#  for the name of models use CapWords
#  for the name of attr snake_case
#  name models singular Role not Roles
#  related_name is for reverse relationship (we can access to User using Role objects)
#  Null is database related.
#  Blank is validation related. (form.is_valid() used here)

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
    price = models.PositiveIntegerField()
    # ! don't use null = True for text-based fields CharField and TextField
    # ! Two possible values for “no data,” that is: None and an empty string.
    description = models.TextField(blank = True) # * Optional

    def __str__(self):
        return self.name

class Table(models.Model):
    name = models.CharField(max_length = 10,unique = True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    waiter_id = models.PositiveIntegerField() # ! how it will take value
    # * table won't be created since it has own create request
    table_id = models.ForeignKey(Table,on_delete=models.CASCADE,related_name = 'orders')
    table_name = models.CharField(max_length=10,blank=True)
    # TODO make this boolean
    isitopen = models.IntegerField(default = 1) # ! how it will take value
    date = models.DateTimeField(default = timezone.now)
    # * all meals will be created in orderedmeals table

    def __str__(self):
        return self.table_id.name

# OrderMeal table is for when
# user ordering meal it will store orderedmeals in this table
class OrderedMeal(models.Model):
    meal_id = models.ForeignKey(Meal,on_delete = models.CASCADE,help_text="It's better to increase count than giving mela id twice or more")
    name = models.CharField(max_length=30)
    count = models.PositiveIntegerField(default=1,blank=True)
    total_sum = models.PositiveIntegerField(null=True,blank=True)
    # * many meal has one order
    order_id = models.ForeignKey(Order,on_delete = models.CASCADE,related_name = 'orderedmeals')

    def __str__(self):
        return self.order_id.table_id.name + ' - ' + self.name + f' ({self.count})'

class Check(models.Model):
    order_id = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='checks')
    # * date will get using Order
    # * meals will get using Order
    servicefee = models.IntegerField(default = 33) # TODO how to generate find out
    # * sum of all meals
    totalsum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.order_id.table_name
        
class ServicePercentage(models.Model):
    percentage=models.IntegerField()

    def __str__(self):
        return self.percentage

class Status(models.Model):
    name = models.CharField(max_length=30,unique = True)
    def __str__(self):
        return self.name