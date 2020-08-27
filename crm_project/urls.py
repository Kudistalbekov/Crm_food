from django.contrib import admin
from django.urls import path

from crm_user.views import(
    UserAPI,
    UserDetailAPI,
    RoleAPI,
    LoginAPI, 
    RoleDetailAPI
)

from crm_app.views  import(
    TableAPI,
    TableDeateilAPI,
    DepartmentAPI,
    DepartmentDetailAPI,
    MealAPI,
    MealDetailAPI,
    MealCategoryAPI,
    MealCategoryDetailAPI,
    StatusAPI,
    StatusDetailAPI,
   
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # user_app 
    path('roles/',RoleAPI.as_view()),
    path('roles/<int:id>/',RoleDetailAPI.as_view()),
    path('users/',UserAPI.as_view()),
    path('users/<int:id>/',UserDetailAPI.as_view()),
    path('login/',LoginAPI.as_view()),
    # crm_app
    path('tables/',TableAPI.as_view()),
    path('tables/<int:id>/',TableDeateilAPI.as_view()),
    path('departments/',DepartmentAPI.as_view()),
    path('departments/<int:id>/',DepartmentDetailAPI.as_view()),
    path('mealCategories/',MealCategoryAPI.as_view()),
    path('mealCategories/<int:id>/',MealCategoryDetailAPI.as_view()),
    path('categoriesByDepartment/<int:id>/',MealCategoryDetailAPI.as_view()),
    path('statuses/',StatusAPI.as_view()),
    path('statuses/<int:id>/',StatusDetailAPI.as_view()),
    path('meals/',MealAPI.as_view()),
    path('meals/<int:id>/',MealDetailAPI.as_view()),
    path('mealsByCategory/<int:id>/',MealDetailAPI.as_view())
]
