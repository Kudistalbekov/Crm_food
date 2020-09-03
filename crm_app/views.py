from django.shortcuts import render
import json # if using Python's built in JSON package, otherwise "import simplejson as json"

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import action

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
                                    )

# Create your views here.
def HandleResponse(data,message,success = True,err = 'no err',resp_status = status.HTTP_200_OK):
    """
    HandleResponse , makes easier to send Response
    Equalent to Response({
            'success':success,
            "error":err,
            "message":message,
            "data":data
        },status = resp_status)
    """
    return Response({
        'success':success,
        "error":err,
        "message":message,
        "data":data
    },status = resp_status)

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
    
    def get_table(self,id):
        try:
            return Table.objects.get(id=id)
        except Table.DoesNotExist:
            return HandleResponse('no data',f"Object {id} is not found",False,resp_status = status.HTTP_404_NOT_FOUND)

    def delete(self,request,id):
        obj=self.get_table(id)

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

    def get_department(self,id):
        try:
            return Department.objects.get(id=id)
        except Department.DoesNotExist:
            return HandleResponse('no data',f"Department {id} does'n exist.",False,resp_status = status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,id):
        data=self.get_department(id)
        if type(data)==Response:
            return data
        data.delete()
        return HandleResponse('no data',f"Department {id} is deleted")

class MealCategoryAPI(APIView):
    
    def get(self,request):
        data = MealCategory.objects.all()
        serializer = MealCategorySeriailizer(data,many=True)
        return HandleResponse(serializer.data,"List of all MealCategories")

    def post(self,request):
        datajson = request.data
        meal_category = MealCategorySeriailizer(data = datajson)
        if meal_category.is_valid():
            meal_category.save()
            return HandleResponse('no data','MealCategory created succesfully',resp_status=status.HTTP_201_CREATED) 
        return HandleResponse('no data','Json format is wrong',False,meal_category.errors,status.HTTP_400_BAD_REQUEST)

class MealCategoryDetailAPI(APIView):
    
    def get_meal_category(self,id):
        try:
            return MealCategory.objects.get(id=id)
        except MealCategory.DoesNotExist:
            return HandleResponse('no data',f'Could not get object {id}',False,'object does not exist',status.HTTP_404_NOT_FOUND)

    def get(self,request,id):
        try:
            Department.objects.get(id = id)
        except Department.DoesNotExist:
            return HandleResponse('no data','Could not find Department with this id',
            False,f'Department does not exist with id {id}',status.HTTP_404_NOT_FOUND)
        department = Department.objects.get(id = id)
        data = department.meal_categories.all()
        serializer = MealCategorySeriailizer(data,many = True)
        return HandleResponse(serializer.data,f'MealCategories with {id} department_id')

    def delete(self,request,id):
        data = self.get_meal_category(id)
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
        try:
            Status.objects.get(id = id)
        except Status.DoesNotExist:
            return HandleResponse('no data','Could not found status',False,'Object does not exist',status.HTTP_404_NOT_FOUND)

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
        serialized_check = MealSerializerUpdate(data = jsondata)
        if serialized_check.is_valid():
            meal_update = Meal.objects.get(id = jsondata['id'])
            for key_val in jsondata:
                setattr(meal_update,key_val,jsondata[key_val])
            meal_update.save()
            return HandleResponse('no data','Meal was updated')
        return HandleResponse('no data',
        'Could not update Meal',False,serialized_check.errors,status.HTTP_400_BAD_REQUEST)

class MealDetailAPI(APIView):
    
    def get(serf,request,id):
        try:
            MealCategory.objects.get(id = id)
        except MealCategory.DoesNotExist:
            return HandleResponse('no data','Could not find Meal_category with this id',
            False,f'Meal_category_id {id} does not exist',status.HTTP_404_NOT_FOUND)

        category = MealCategory.objects.get(id = id)
        data = category.meals.all()

        s = MealSerializer(data,many = True)
        return HandleResponse(s.data,f'List of Meals with category_id {id}')

    def delete(self,request,id):
        try:
            Meal.objects.get(id=id)
        except Meal.DoesNotExist:
            return HandleResponse('no data',
                                    'Could not find Meal with this id',
                                    False,
                                    f'Meal with id = {id} does not exist',
                                    status.HTTP_404_NOT_FOUND)
        meal = Meal.objects.get(id = id)
        meal.delete()
        return HandleResponse('no data','Meal was deleted successfully')

class ServicePercentageAPI(APIView):
    pass

class ServicePercentageDetail(APIView):
    pass

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
        check.delete()
        return HandleResponse('no data','Check was deleted')

class MealsToOrderAPI(APIView):
    def post(self,request):
        try:
            Order.objects.get(id=request.data.get('order_id'))
        except:
            return HandleResponse('no data','Order with this id does not exist',False,'not found order',status.HTTP_404_NOT_FOUND)
        # * we can use "context" to pass extra value
        serializer = OrdersOrderedMealSerializer(data = request.data, context={'order_id': request.data.get('order_id')})
        if serializer.is_valid():
            return HandleResponse('no data','meals added',resp_status=status.HTTP_201_CREATED)
        return HandleResponse('no data','Could not add meals',False,serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        return HandleResponse('no data','Ordered meal is deleted')

class MealsToOrderDetailAPI(APIView):
    def get(self,request,id):
        try:
            Order.objects.get(id = id)
        except Order.DoesNotExist:
            return HandleResponse('no data','Could not get data',False,'order does not exist',status.HTTP_404_NOT_FOUND)
        order = Order.objects.get(id = id)
        serializer = OrdersOrderedMealSerializer(order)
        return HandleResponse(serializer.data,'List of ordered_meal of order')