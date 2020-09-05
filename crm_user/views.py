from django.shortcuts import render
import json # if using Python's built in JSON package, otherwise "import simplejson as json"

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from crm_user.models import MyUser as User , UserRole as Role
from django.contrib.auth import login
from django.shortcuts import render

# Create your views here

from crm_user.serializers import(
    RoleSerializer,
    UpdateUserSerializer,
    UserSerializer,
    LoginSerializer
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


class RoleAPI(APIView):
    
    def get(self,request):
        data = Role.objects.all()
        serializer = RoleSerializer(data,many=True)
        return HandleResponse(serializer.data,'Given all Roles')
    
    def post(self,request):
        data = request.data
        serializer = RoleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return HandleResponse('no data','New Role is created',resp_status=status.HTTP_201_CREATED)
        return HandleResponse('no data','Could not create a Role',False,serializer.errors,status.HTTP_400_BAD_REQUEST)

class RoleDetailAPI(APIView):

    def get_role(self,id):
        try:
            return Role.objects.get(id=id)
        except Role.DoesNotExist:
            return HandleResponse('no data',f"Role {id} is not found",False,resp_status = status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,id):
        data = self.get_role(id)
        if type(data) == Response:
            return data
        data.delete()
        return HandleResponse('no data',f"Role {id} is deleted")

class UserAPI(APIView):
    
    def get_user(self,id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return HandleResponse(
                'no data',
                'Could not find User',
                err = f"User {id} does not exist",
                resp_status=status.HTTP_404_NOT_FOUND)

    def get(self,request):
        data = User.objects.all()
        serializer = UserSerializer(data,many=True)
        return HandleResponse(serializer.data,'Given all Users')

    def post(self,request):
        jsondata = request.data
        # * since we are passing just data it will call serializers create functions
        data = UserSerializer(data=jsondata)
        if data.is_valid():
            user = data.save()
            return HandleResponse(user.login,'User is created',resp_status=status.HTTP_201_CREATED)
        return HandleResponse('no data','Could not create User',False,data.errors,status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        jsondata = request.data
        user = self.get_user(jsondata['id'])
        
        if type(user) == Response:
            return user
        
        # * since we are passing instance and validated_data
        # * method save will call update method

        serializer = UpdateUserSerializer(user,data = jsondata)
        if serializer.is_valid():
            serializer.save()
            return HandleResponse('no data','User was updated',resp_status=status.HTTP_200_OK)
        return HandleResponse('no data','Json format is wrong',True,serializer.errors,status.HTTP_404_NOT_FOUND)
    
    # ! PUT is for updating entire resourse
    # ! PATCH is for updating just some fields    
    
    def patch(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data["user"]
        newpassword = request.data.get('newpassword',"")
        if not(newpassword):
            return HandleResponse('nodata','newpassword has to be given',False,'newpassword missed',status.HTTP_400_BAD_REQUEST)
        user.set_password(newpassword)
        user.save()
        return HandleResponse({"login":user.login},'Password is changed')

class UserDetailAPI(APIView):
    
    def get_user(self,id):
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return HandleResponse(
                'no data',
                'Could not find User',
                err = f"User {id} does not exist",
                resp_status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,id):
        data = self.get_user(id)

        if type(data) == Response:
            return data

        data.delete()
        return HandleResponse('no data',f"User {id} deleted",resp_status = status.HTTP_200_OK)

class LoginAPI(APIView):

    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data["user"]
        login(request,user)
        token,created = Token.objects.get_or_create(user = user)
        return HandleResponse({"token":token.key},"Token of user")
