from rest_framework import serializers
from crm_user.models import MyUser,UserRole
from rest_framework import exceptions 
from django.contrib.auth import authenticate

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('id','name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','name','surname','password','login','email','roleid','dateofadd','phone']
        extra_kwargs = {'password':{'write_only':True}}

class UpdateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False,write_only = True)
    name = serializers.CharField(required=False,write_only = True)
    surname = serializers.CharField(required=False,write_only = True)
    password = serializers.CharField(required=False,write_only = True)
    login = serializers.CharField(required=False,write_only = True)
    email = serializers.CharField(required=False,write_only = True)
    roleid = serializers.CharField(required=False,write_only = True)
    phone = serializers.CharField(required=False,write_only = True)

class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        login = data.get("login","")
        password = data.get("password","")
        
        if login and password:
            user = authenticate(username = login,password = password)
            if user:
                if user.is_active:
                    data["user"]=user
                else:
                    msg =  'account is disabled'
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with this login_name"
                raise exceptions.ValidationError(msg)
        else:
            msg = "User must provide login and password"
            raise exceptions.ValidationError(msg)
        return data