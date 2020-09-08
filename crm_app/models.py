from django.db import models
from django.utils import timezone
from crm_user.models import MyUser
from rest_framework.response import Response
from rest_framework import status 
from crm_app.functions import HandleResponse
from crm_app.managers import *

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
    
    objects = DepartmentManager()
    
    def __str__(self):
        return self.name

class MealCategory(models.Model):
    
    name = models.CharField(max_length=30,unique=True)
    department_id = models.ForeignKey(Department,on_delete=models.CASCADE,related_name='meal_categories')    

    objects = MealCategoryManager()

    def __str__(self):
        return self.name
        
class Meal(models.Model):
    
    name = models.CharField(max_length=30,unique=True)
    #* MealCategory can have many meals 
    #* meal in one category
    category_id = models.ForeignKey(MealCategory,on_delete=models.CASCADE,related_name='meals')
    price = models.PositiveIntegerField()
    # ! don't use null = True for text-based fields CharField and TextField
    # ! Two possible values for “no data,” that is: None and an empty string.
    description = models.TextField(blank = True) # * Optional

    objects = MealManager()

    def __str__(self):
        return self.name

class Table(models.Model):
    
    # user can have many tables to serve
    # * User can serve several tables
    # * Table is served by one user
    user_id = models.ForeignKey(MyUser,on_delete = models.SET_NULL,null=True,related_name='tebles')
    name = models.CharField(max_length = 10,unique = True)
    
    objects = TableManager()
    def __str__(self):
        return self.name

class Order(models.Model):
    
    # * User can have many orders 
    # * one order is served by one Waiter
    
    waiter_id = models.ForeignKey(
        MyUser,
        null = True,
        blank = True,
        on_delete = models.PROTECT,
        related_name = 'orders') 

    # * table won't be created since it has own create request
    # * Table can have order
    # * specific order in one table

    table_id = models.OneToOneField(
        Table,
        on_delete = models.PROTECT,
        related_name = 'orders',
        error_messages = {'invalid':'order in this table is olready crated,use mealsToOrder to add meals'})
    
    table_name = models.CharField(max_length=10,blank=True)
    # TODO make this boolean
    my_choices = [(1,True),(0,False)]
    isitopen = models.BooleanField(choices = my_choices ,default = 1) # ! how it will take value
    date = models.DateTimeField(default = timezone.now)
    
    objects = OrderManager()
    
    # * all meals will be created in orderedmeals table
    def __str__(self):
        return self.table_id.name
    
    def func(self):
        return self.table_name

# OrderMeal table is for when
# user ordering meal it will store orderedmeals in this table

class OrderedMeal(models.Model):

    # * Meal can have many orderedmeal
    # * specificorderedmeal can have one meal
    # * many orderedmeal have one meal

    meal_id = models.ForeignKey(
        Meal,
        on_delete = models.CASCADE,
        help_text = "It's better to increase count than giving meal id twice or more")

    name = models.CharField(max_length=30)
    count = models.PositiveIntegerField(default=1,blank=True)
    total_sum = models.PositiveIntegerField(null=True,blank=True)
    # * many orderedmeal have one order
    order_id = models.ForeignKey(Order,on_delete = models.CASCADE,related_name = 'orderedmeals')

    objects = OrderedMealManager()

    def __str__(self):
        return self.order_id.table_id.name + ' - ' + self.name + f' ({self.count})'
    
    def set_total_sum(self):
        '''Sets the sum of each meal'''
        meal = Meal.objects.get(id = getattr(self.meal_id,'id'))
        self.total_sum = self.count*int(meal.price)
        self.save()
        return self.total_sum

class ServicePercentage(models.Model):
    
    percentage = models.IntegerField()

    def __str__(self):
        return str(self.percentage)

class Check(models.Model):
    order_id = models.OneToOneField(Order,on_delete = models.CASCADE,related_name='ordercheck')
    
    # * date will get using Order
    # * meals will get using Order

    # TODO how to generate find out
    servicefee = models.ForeignKey(ServicePercentage,on_delete = models.SET_NULL,null = True) 
    # * sum of all meals
    totalsum = models.PositiveIntegerField(default=0)

    objects = CheckManager()

    def __str__(self):
        return self.order_id.table_name
    
    def set_totalsum(self):
        '''Sets the sum of check'''
        order = Order.objects.get(id = self.order_id.id)
        self.totalsum = 0
        self.save()  
        for meals in order.orderedmeals.all():
            print(f'{self.totalsum}+{meals.total_sum}={self.totalsum + meals.total_sum}')
            self.totalsum=int(self.totalsum)+int(meals.total_sum)
        self.save()  
        return self.totalsum

class Status(models.Model):
    name = models.CharField(max_length=30,unique = True)
    
    objects = StatusManager()

    def __str__(self):
        return self.name