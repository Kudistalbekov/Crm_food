from crm_app.models import (
    Department,
    MealCategory,
    Meal,
    Table,
    Order,
    Check,
    ServicePercentage,
    Status,
    OrderedMeal)

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

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id','name')

    def create(self,validated_data):
        return Table.objects.create(**validated_data)

class OrderedMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedMeal
        fields = ['meal_id','name','count']

class OrderSerializer(serializers.ModelSerializer):
    # TODO remember this
    # * orderedmeals is taken from reverse lookup name field
    # * from table OrderedMeals from field order_id
    # * since order_id has related_name we have to use that name
    # * if doesn't have user order_it_set

    orderedmeals = OrderedMealSerializer(many = True)
    class Meta:
        model = Order
        # ! added waiter_id and isitopen by myself.
        fields = ('id','waiter_id','table_id','table_name','isitopen','date','orderedmeals')
        
    def create(self,validated_data):
        orderedmeals = validated_data.pop('orderedmeals')
        order = Order.objects.create(**validated_data)
        # * fill table_name
        table = Table.objects.get(id = getattr(order.table_id,'id'))
        order.table_name = table.name
        order.save()
        # * creating ordered_meals
        for orderedmeal in orderedmeals:
            # * Here we are saying create new ordered_meal
            # * whicn has order_id = id of given order
            new_ordered = OrderedMeal.objects.create(**orderedmeal,order_id = order)
            meal = Meal.objects.get(id = getattr(new_ordered.meal_id,'id'))
            new_ordered.total_sum = new_ordered.count*int(meal.price)
            new_ordered.save()

        return order

class MealSerializerUpdate(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    category_id = serializers.IntegerField(required=False)
    price = serializers.CharField(required=False)
    description = serializers.CharField(required=False,allow_blank=True)

class CheckSerializer(serializers.ModelSerializer):
    order_id = OrderSerializer()
    class Meta:
        model = Check
        fields = ('id','order_id','servicefee','totalsum')
    
    # TODO add price of meal
    def to_representation(self,data):
        new_data = super(CheckSerializer,self).to_representation(data)
        return {
            "id":new_data['id'],
            "ordered_id":new_data['order_id']['id'],
            "date":new_data['order_id']['date'],
            "servicefee":new_data['servicefee'],
            "totalsum":new_data['totalsum'],
            "meals":new_data['order_id']['orderedmeals']
        }

class CheckPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"
    
    def create(self,validated_data):
        check = Check.objects.create(**validated_data)
        order = Order.objects.get(id = validated_data.get('order_id').id)
        for meals in order.orderedmeals.all():
            check.totalsum=int(check.totalsum)+int(meals.total_sum)
        check.save()            
        return check

class ServicePercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePercentage
        fields = ('id','percentage')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id','name')