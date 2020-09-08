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
        fields = ['id','name','surname','login','email','roleid','phone']
        extra_kwargs = {'phone': {'required': True},'roleid':{'required':True}}

    def create(self, validated_data):
        '''method for creating user'''
        name = validated_data.get('name')
        surname = validated_data.get('surname')
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        # * im giving phone number as password for the first password
        user = MyUser.objects.create_user(name+'_'+surname,email,phone)
        user.name = name
        user.surname = surname
        user.roleid = validated_data.get('roleid')
        user.phone = phone
        user.save()
        return user

class UpdateUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False,write_only = True)
    name = serializers.CharField(required=False,write_only = True)
    surname = serializers.CharField(required=False,write_only = True)
    login = serializers.CharField(required=False,write_only = True)
    email = serializers.CharField(required=False,write_only = True)
    roleid = serializers.CharField(required=False,write_only = True)
    phone = serializers.CharField(required=False,write_only = True)

    def update(self,user, validated_data):
        # * validated_data.get(arg1,arg2) means
        # * it will try to take from validated_data arg1 
        # * if arg1 does not there it will take by default arg2

        user.name = validated_data.get('name',user.name)
        user.surname = validated_data.get('surname',user.surname)
        user.login = validated_data.get('login',user.login)
        user.email = validated_data.get('email',user.email)
        user.roleid = validated_data.get('roleid',user.roleid)
        user.phone = validated_data.get('phone',user.phone)
        user.save()
        
        return user

class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        login = data.get("login","")
        password = data.get("password","")
        
        if login and password:
            # * authentication
            user = authenticate(username = login,password = password)
            if user:
                if user.is_active:
                    data["user"] = user
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