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
from rest_framework.response import Response

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

    def update(self,meal,validated_data):

        for key_val in validated_data:
            setattr(meal,key_val,validated_data.get(key_val))

        meal.save()
        return meal

class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ('id','user_id','name')
        extra_kwargs = {'user_id': {'write_only' : True}}
        

    def create(self,validated_data):
        return Table.objects.create(**validated_data)

class OrderedMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedMeal
        fields = ['meal_id','name','count']
        extra_kwargs = {'name': {'required': False}}

    # * update will be used when deleting ordered_meal
    # TODO (1) if orderedmeal in db decrease (count,total_sum)
    # TODO (2) if orderedmeal in db and count is 1 delete ordered meal
    def update(self,orderedmeal,validated_data):
        check = Check.objects.get(order_id = orderedmeal.order_id)
        # {2}
        # if count not given , delete 1 meal
        if (
            orderedmeal.count == 1 or 
            orderedmeal.count <= validated_data.get('count')):
            orderedmeal.delete()
            return orderedmeal
        # {1}
        orderedmeal.count -= validated_data.get('count',1)
        orderedmeal.total_sum = orderedmeal.count*int(self.context['meal'].price)
        orderedmeal.save()
        check.set_totalsum()
        return orderedmeal
    
class OrdersOrderedMealSerializer(serializers.ModelSerializer):
        orderedmeals = OrderedMealSerializer(many = True)
        class Meta:
            model = Order
            fields = ['id','orderedmeals']
    
        #TODO {1} create orderedmeal if does not exist
        #TODO {2} if ordered meal exist increase count
        #TODO {3} check the names of ordered meals if they don't match return error 
        #TODO {4} update check for the current order if exist

        # * validate will be used when creating orderedmeal
        def validate(self,validated_data):
            order = Order.objects.get(id = self.context['order_id'])
            check_order = Check.objects.get(order_id = order)
            ordered_meal = OrderedMeal()
            for orderedmeal in validated_data['orderedmeals']:
                # {3}
                try:
                    Meal.objects.get(id = orderedmeal['meal_id'].id,name = orderedmeal['name'])
                except Meal.DoesNotExist:
                    err = f'name ({orderedmeal["name"]}) does not match with meal.name'
                    raise serializers.ValidationError({'name error':err})
                # {1}
                try:
                    OrderedMeal.objects.get(order_id = order,meal_id = orderedmeal['meal_id'])
                except OrderedMeal.DoesNotExist:
                    print('ordered meal does not exist creating')
                    new_ordered = OrderedMeal.objects.create(**orderedmeal,order_id = order)
                    new_ordered.set_total_sum()
                    continue
                #{2}
                ordered_meal = OrderedMeal.objects.get(order_id = order,meal_id = orderedmeal['meal_id']) 
                ordered_meal.count+=orderedmeal.get('count',1)
                ordered_meal.set_total_sum()
            # updating check 
            check_order.set_totalsum()
            return ordered_meal

 
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
        extra_kwargs = {'waiter_id': {'required': False},'isitopen_id':{'required': False}}

    def create(self,validated_data):
        orderedmeals = validated_data.pop('orderedmeals')
        order = Order.objects.create(**validated_data)
        # TODO fill table_name,waiter_for this order,is_it_open
        table = Table.objects.get(id = getattr(order.table_id,'id'))
        order.waiter_id = table.user_id
        order.table_name = table.name
        order.save()
        # * creating ordered_meals
        for orderedmeal in orderedmeals:
            # * Here we are saying create new ordered_meal
            # * whicn has order_id = id of given order
            print(orderedmeal)
            meal = OrderedMeal.objects.get_orderedmeal(order = order,meal = orderedmeal['meal_id'])
            if type(meal) == Response:
                # no found
                new_ordered = OrderedMeal.objects.create(**orderedmeal,order_id = order)
                new_ordered.set_total_sum()
                continue
            meal.count+=orderedmeal.get('count')
            meal.set_total_sum()
            meal.save()
        return order



class OrderedCheckMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedMeal
        fields = ['meal_id','name','count','total_sum']
    
    def to_representation(self,data):
        new_data = super(OrderedCheckMealSerializer,self).to_representation(data)
        meal = Meal.objects.get(id = new_data['meal_id'])
        return {
            'meal_id':new_data['meal_id'],
            'name':new_data['name'],
            'price':meal.price,
            'count':new_data['count'],
            'total_sum':new_data['total_sum']
        }

class OrderCheckSerializer(serializers.ModelSerializer):
    orderedmeals = OrderedCheckMealSerializer(many = True)
    class Meta:
        model = Order
        fields = ('id','date','orderedmeals')

class ServicePercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePercentage
        fields = ('id','percentage')

class CheckSerializer(serializers.ModelSerializer):
    order_id = OrderCheckSerializer()
    servicefee = ServicePercentageSerializer()
    class Meta:
        model = Check
        fields = ('id','order_id','servicefee','totalsum')


    def to_representation(self,data):
        new_data = super(CheckSerializer,self).to_representation(data)
        return {
            "id":new_data['id'],
            "ordered_id":new_data['order_id']['id'],
            "date":new_data['order_id']['date'],
            "servicefee":new_data['servicefee']['percentage'],
            "totalsum":new_data['totalsum'],
            "meals":new_data['order_id']['orderedmeals']
        }

class CheckPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"
    
    def create(self,validated_data):
        check = Check.objects.create(**validated_data)
        servefee = ServicePercentage.objects.all().first()
        check.servicefee = servefee
        check.set_totalsum()          
        return check

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id','name')