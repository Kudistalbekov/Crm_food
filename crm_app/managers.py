from crm_app.models import * 


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

