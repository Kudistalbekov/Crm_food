from django.shortcuts import render
import json # if using Python's built in JSON package, otherwise "import simplejson as json"

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import action
from crm_app.functions import HandleResponse

from crm_app.models import (
                            Department,
                            Meal,
                            MealCategory,
                            Table,
                            Order,
                            Check,
                            ServicePercentage,
                            Status,
                            OrderedMeal)

from crm_app.serializers import (
                                    TableSerializer,
                                    DepartmentSerializer,
                                    MealCategorySeriailizer,
                                    StatusSerializer,
                                    MealSerializer,
                                    MealSerializerUpdate,
                                    OrderSerializer,
                                    CheckSerializer,
                                    CheckPostSerializer,
                                    OrderedMealSerializer,
                                    OrdersOrderedMealSerializer,
                                    ServicePercentageSerializer,
                                    )

class TableAPI(APIView):
    def get(self,request):
        data = Table.objects.all()
        serializer = TableSerializer(data,many=True)
        return HandleResponse(serializer.data,'Given all tables')
    
    def post(self,request):
        data = request.data
        serializer = TableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return HandleResponse('no data','New Table is created',True,'no error',status.HTTP_201_CREATED)
        return HandleResponse("no data",'Could not create a Table',False,serializer.errors,status.HTTP_404_NOT_FOUND)

class TableDeateilAPI(APIView):
    def delete(self,request,id):
        obj = Table.objects.get_table(id=id)
        #if object is not exist return the returned error
        if type(obj) == Response:
            return obj
        
        obj.delete()
        return HandleResponse('no data',f"Table {id} is deleted")

class DepartmentAPI(APIView):
    def get(self,request):
        data = Department.objects.all()
        serializer = DepartmentSerializer(data,many=True)
        return HandleResponse(serializer.data,'Given all Departments')
    
    def post(self,request):
        data = request.data
        serializer = DepartmentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return HandleResponse('nodata','Department is created')
        return HandleResponse('no data','Could not create a new Department',False,serializer.errors,status.HTTP_400_BAD_REQUEST)

class DepartmentDetailAPI(APIView):
    def delete(self,request,id):
        data = Department.objects.get_department(id)
        if type(data) == Response:
            return data
        data.delete()
        return HandleResponse('no data',f"Department {id} is deleted")

class MealCategoryAPI(APIView):
    
    def get(self,request):
        data = MealCategory.objects.all()
        serializer = MealCategorySeriailizer(data,many=True)
        return HandleResponse(serializer.data,"List of all MealCategories")

    def post(self,request):
        meal_category = MealCategorySeriailizer(data = request.data)
        if meal_category.is_valid():
            meal_category.save()
            return HandleResponse('no data','MealCategory created succesfully',resp_status=status.HTTP_201_CREATED) 
        return HandleResponse('no data','Json format is wrong',False,meal_category.errors,status.HTTP_400_BAD_REQUEST)

class MealCategoryDetailAPI(APIView):
    def get(self,request,id):
        department = Department.objects.get_department(id = id)

        if type(department) == Response:
            return department

        data = department.meal_categories.all()
        serializer = MealCategorySeriailizer(data,many = True)
        return HandleResponse(serializer.data,f'MealCategories with {id} department_id')

    def delete(self,request,id):
        data = MealCategory.objects.get_meal_category(id)

        if not(type(data)==Response):
            data.delete()
            return HandleResponse('no data',f'MealCategory {id} is deleted')

        return data

class StatusAPI(APIView):
    
    def get(self,request):
        data = Status.objects.all()
        serializer = StatusSerializer(data,many = True)
        return HandleResponse(serializer.data,'Given all statuses')
    
    def post(self,request):
        jsondata = request.data
        serializer = StatusSerializer(data=jsondata)
        if serializer.is_valid():
            serializer.save()
            return HandleResponse('no data','Status was created',resp_status=status.HTTP_201_CREATED)
        return HandleResponse('no data','Could not create Status',False,serializer.errors,status.HTTP_400_BAD_REQUEST)

class StatusDetailAPI(APIView):
    
    def delete(self,request,id):
        status = Status.objects.get_status(id = id)
        
        if status == Response:
            return status

        obj = Status.objects.get(id=id)
        obj.delete()
        return HandleResponse('no data','Status successfully deleted')        

class MealAPI(APIView):
    
    def get(self,request):
        data = Meal.objects.all()
        serialized = MealSerializer(data,many = True)
        return HandleResponse(serialized.data,'List of Meals')

    def post(self,request):
        jsondata = request.data
        serialized = MealSerializer(data = jsondata)
        if serialized.is_valid():
            serialized.save()
            return HandleResponse('no data','Created new Meal',status.HTTP_201_CREATED)
        return HandleResponse('no data','Could not create Meal',False,serialized.errors,status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        jsondata = request.data
        meal_update = Meal.objects.get(id = jsondata['id'])
        serialized_check = MealSerializerUpdate(meal_update,data = jsondata)
        
        if serialized_check.is_valid():
            serialized_check.save()
            return HandleResponse('no data','Meal was updated')

        return HandleResponse('no data',
        'Could not update Meal',False,serialized_check.errors,status.HTTP_400_BAD_REQUEST)

class MealDetailAPI(APIView):
    
    def get(serf,request,id):
        data = MealCategory.objects.get_meal_category(id)
        if not(type(data)==Response):
            category = MealCategory.objects.get(id = id)
            data = category.meals.all()
            s = MealSerializer(data,many = True)
            return HandleResponse(s.data,f'List of Meals with category_id {id}')
        return data

    def delete(self,request,id):
        meal = Meal.objects.get_meal(id = id)
        if not type(meal)==Response:
            meal.delete()
            return HandleResponse('no data','Meal was deleted successfully')
        return meal

class ServicePercentageAPI(APIView):

    def get(self,request):
        data = ServicePercentage.objects.all()
        ser = ServicePercentageSerializer(data,many = True)
        return HandleResponse(ser.data,'ServicePercentage list')

    # * when post called i will update same servicepercentage
    # * no need to create new
    def post(self,request):
        ser = ServicePercentageSerializer(data = request.data)
        if ser.is_valid():
            ser.save()
            return HandleResponse('Added','ServicePercentage created',resp_status = status.HTTP_201_CREATED)
        return HandleResponse('no data','Could not add',False,ser.errors,status.HTTP_400_BAD_REQUEST)

class ServicePercentageDetailAPI(APIView):

    def delete(self,request,id):
        percentage = ServicePercentage.objects.get(id = id)
        percentage.delete()
        return HandleResponse('no data','Service Percentage Deleted')

class OrderAPI(APIView):
    def get(self,request):
        data = Order.objects.all()
        serialized = OrderSerializer(data,many = True)
        return HandleResponse(serialized.data,'List of Orders')

    def post(self,request):
        data = request.data
        serializer = OrderSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return HandleResponse('no data','New order is created !',resp_status=status.HTTP_201_CREATED)
        return HandleResponse('no data','New order could not be created',False,serializer.errors,status.HTTP_400_BAD_REQUEST) 

class OrderDetailAPI(APIView):
    
    def delete(self,request,id):
        try:
            Order.objects.get(id=id)
        except Order.DoesNotExist:
            return HandleResponse('no data','Could not get data',False,'order does not exist',status.HTTP_404_NOT_FOUND)
        
        order = Order.objects.get(id=id)
        order.delete()
        return HandleResponse('no data','Order is deleted')

class GetOpenStatusAPI(APIView):
    
    def get(self,request):
        data = Order.objects.filter(isitopen = 1)
        serializer = OrderSerializer(data,many=True)
        return HandleResponse(serializer.data,'List of opened orders')

class CheckAPI(APIView):

    def get(self,request):
        data = Check.objects.all()
        check = CheckSerializer(data,many = True)
        return HandleResponse(check.data,'List of all checks')

    def post(self,request):
        serializer_check = CheckPostSerializer(data=request.data)
        if serializer_check.is_valid():
            serializer_check.save()
            return HandleResponse(serializer_check.data,
            'Check is created',resp_status=status.HTTP_201_CREATED)
        return HandleResponse('no data','Could not create check',False,serializer_check.errors,status.HTTP_400_BAD_REQUEST)

class CheckDetailAPI(APIView):

    def delete(self,request,id):
        try:
            Check.objects.get(id = id)
        except Check.DoesNotExist:
            return HandleResponse('no data','Could not Delete',False,'Does not exist',status.HTTP_404_NOT_FOUND)

        check = Check.objects.get(id = id)
        order = Order.objects.get(id = getattr(check.order_id,'id'))
        order.delete()
        check.delete()
        return HandleResponse('no data','Check was deleted')

class MealsToOrderAPI(APIView):

    def post(self,request):
        order = Order.objects.get_order(request.data.get('order_id'))
        if type(order) == Response:
            return order
        # * we can use "context" to pass extra value
        serializer = OrdersOrderedMealSerializer(data = request.data, context={'order_id': request.data.get('order_id')})
        if serializer.is_valid():
            return HandleResponse('no data','meals added',resp_status=status.HTTP_201_CREATED)
        return HandleResponse('no data','Could not add meals',False,serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    # deleting ordered meal
    def put(self,request):
        order = Order.objects.get_order(request.data.get('order_id'))
        meal = Meal.objects.get_meal(request.data.get('meal_id'))

        if type(order) == Response:
            return order
        
        if type(meal) == Response:
            return meal
            
        # updating ordered meals
        ordered_meal = OrderedMeal.objects.get_orderedmeal(order,meal)
        
        if type(ordered_meal) == Response:
            return ordered_meal

        serilizer = OrderedMealSerializer(ordered_meal,data = request.data,context = {'meal':meal})
        if serilizer.is_valid():
            # updating and creating will be on .save() method
            serilizer.save()
            return HandleResponse('no data','Ordered meal is deleted')
        
        return HandleResponse(
            'no data',
            'Ordered meal could not be deleted',
            False,
            serilizer.errors,
            status.HTTP_400_BAD_REQUEST)

class MealsToOrderDetailAPI(APIView):
    def get(self,request,id):
        order = Order.objects.get_order(id = id)
        if type(order) == Response:
            return order
        serializer = OrdersOrderedMealSerializer(order)
        return HandleResponse(serializer.data,'List of ordered_meal of order')