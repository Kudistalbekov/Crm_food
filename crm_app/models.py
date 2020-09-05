from django.db import models
from django.utils import timezone
from crm_user.models import MyUser
from rest_framework.response import Response
from rest_framework import status 

def HandleResponse(data,message,success = True,err = 'no err',resp_status = status.HTTP_200_OK):
    return Response({
        'success':success,
        "error":err,
        "message":message,
        "data":data
    },status = resp_status)


class DepartmentManager(models.Manager):
    def get_department(self,id):
        try:
            return Department.objects.get(id=id)
        except Department.DoesNotExist:
            return HandleResponse('no data',f"Department {id} does'n exist.",False,resp_status = status.HTTP_404_NOT_FOUND)

class MealCategoryManager(models.Manager):
    def get_meal_category(self,id):
        try:
            return MealCategory.objects.get(id=id)
        except MealCategory.DoesNotExist:
            return HandleResponse('no data',f'Could not get object {id}',False,'object does not exist',status.HTTP_404_NOT_FOUND)


class MealManager(models.Manager):
    def get_meal(self,id):
        try:
            return Meal.objects.get(id = id)
        except Meal.DoesNotExist:
            return HandleResponse('no data','Meal with this id does not exist',False,'not found Meal',status.HTTP_404_NOT_FOUND)


class TableManager(models.Manager):
    def get_table(self,id):
        try:
            return Table.objects.get(id=id)
        except Table.DoesNotExist:
            return HandleResponse('no data',f"Object {id} is not found",False,resp_status = status.HTTP_404_NOT_FOUND)


class OrderManager(models.Manager):
    def get_order(self,id):
        try:
            return Order.objects.get(id = id)
        except Order.DoesNotExist:
            return HandleResponse('no data','Order with this id does not exist',False,'not found order',status.HTTP_404_NOT_FOUND)


class OrderedMealManager(models.Manager):
    def get_orderedmeal(self,order,meal):
        try:
            return OrderedMeal.objects.get(order_id = order,meal_id = meal)
        except OrderedMeal.DoesNotExist:
            return HandleResponse('no data','OrderedMeal with this credential does not exist',False,'not found Meal',status.HTTP_404_NOT_FOUND)


class CheckManager(models.Manager):
    def get_department(self,id):
        try:
            return Check.objects.get(id=id)
        except Check.DoesNotExist:
            return HandleResponse('no data',f"Check {id} does'n exist.",False,resp_status = status.HTTP_404_NOT_FOUND)

class StatusManager(models.Manager):
    def get_status(self,id):
        try:
            return Status.objects.get(id=id)
        except Status.DoesNotExist:
            return HandleResponse('no data',f"Status {id} does'n exist.",False,resp_status = status.HTTP_404_NOT_FOUND)

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
    user_id = models.ForeignKey(MyUser,on_delete = models.SET_NULL,null=True,related_name='tebles')
    name = models.CharField(max_length = 10,unique = True)
    
    objects = TableManager()
    def __str__(self):
        return self.name

class Order(models.Model):
    
    waiter_id = models.ForeignKey(
        MyUser,
        null = True,
        blank = True,
        on_delete = models.PROTECT,
        related_name = 'orders') 

    # * table won't be created since it has own create request
    table_id = models.ForeignKey(Table,on_delete = models.PROTECT,related_name = 'orders')
    
    table_name = models.CharField(max_length=10,blank=True)
    # TODO make this boolean
    isitopen = models.IntegerField(default = 1) # ! how it will take value
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
    meal_id = models.ForeignKey(
        Meal,
        on_delete = models.CASCADE,
        help_text="It's better to increase count than giving meal id twice or more")

    name = models.CharField(max_length=30)
    count = models.PositiveIntegerField(default=1,blank=True)
    total_sum = models.PositiveIntegerField(null=True,blank=True)
    # * many meal has one order
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
        return self.percentage

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