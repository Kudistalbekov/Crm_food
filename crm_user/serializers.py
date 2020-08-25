from rest_framework import serializers
from crm_user.models import MyUser,UserRole

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
