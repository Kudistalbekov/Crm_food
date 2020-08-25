from crm_app.models import Department,MealCategory,Meal,Table,Order,Check,ServicePercentage,Status
from rest_framework import serializers , fields

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id','name')
    

class MealCategorySeriailizer(serializers.ModelSerializer):
    class Meta:
        model = MealCategory
        fields = ('id','name','department_id')

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal 
        fields = ['id','name','category_id','price','description']

class MealSerializerUpdate(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    category_id = serializers.IntegerField(required=False)
    price = serializers.CharField(required=False)
    description = serializers.CharField(required=False,allow_blank=True)

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id','name')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','waiterid','tableid','tablename','isitopen','date','meals')

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ('id','order_id','date','servicefee','totalsum','meals')

class ServicePercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePercentage
        fields = ('id','percentage')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id','name')