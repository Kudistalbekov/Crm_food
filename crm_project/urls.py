"""crm_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from crm_user.views import(
    UserAPI,
    UserDetailAPI,
    RoleAPI,
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
    path('tables/',TableAPI.as_view()),
    path('tables/<int:id>/',TableDeateilAPI.as_view()),
    path('roles/',RoleAPI.as_view()),
    path('roles/<int:id>/',RoleDetailAPI    .as_view()),
    path('departments/',DepartmentAPI.as_view()),
    path('departments/<int:id>/',DepartmentDetailAPI.as_view()),
    path('users/',UserAPI.as_view()),
    path('users/<int:id>/',UserDetailAPI.as_view()),
    path('mealCategories/',MealCategoryAPI.as_view()),
    path('mealCategories/<int:id>/',MealCategoryDetailAPI.as_view()),
    path('categoriesByDepartment/<int:id>/',MealCategoryDetailAPI.as_view()),
    path('statuses/',StatusAPI.as_view()),
    path('statuses/<int:id>/',StatusDetailAPI.as_view()),
    path('meals/',MealAPI.as_view()),
    path('meals/<int:id>/',MealDetailAPI.as_view()),
    path('mealsByCategory/<int:id>/',MealDetailAPI.as_view())
]
