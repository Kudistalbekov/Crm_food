from django.shortcuts import render
import json # if using Python's built in JSON package, otherwise "import simplejson as json"

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import action
from crm_user.models import MyUser as User , UserRole as Role
# Create your views here.
from crm_user.serializers import(
    RoleSerializer,
    UpdateUserSerializer,
    UserSerializer
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
        data = UserSerializer(data=jsondata)
        if data.is_valid():
            ser_user = data.save()

            user = User.objects.get(id = ser_user.id)
            user.login = user.name + '_' + user.surname
            user.password = user.phone
            user.save()
            
            return HandleResponse(user.login,'User is created',resp_status=status.HTTP_201_CREATED)
        return HandleResponse('no data','Could not create User',False,data.errors,status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        jsondata = request.data
        serializer = UpdateUserSerializer(data = jsondata)
        if serializer.is_valid():
            user = self.get_user(jsondata['id'])
            if not(type(user) == Response):
                # updating the user
                for o in jsondata:
                    setattr(user,o,jsondata[o])
                user.save()
                return HandleResponse('no data','User was updated',resp_status=status.HTTP_200_OK)
            return user
        return HandleResponse('no data','Json format is wrong',True,serializer.errors,status.HTTP_404_NOT_FOUND)

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

