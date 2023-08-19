from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import json
import time
class SER_Users_R(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number','invite_code','referred_by')

class SER_Users_U(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ('id','phone_number','referred_by')
    

class SER_Users_C_1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','phone_number','referred_by')

class SER_Users_C_2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','auth_code_2',)

class AuthTokenSystem(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['phone_number'] = user.phone_number

        return token
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        
        if 'password' not in attrs.keys():
            attrs.update({'password': "nothing"})
        return super(AuthTokenSystem, self).validate(attrs)
    

        
    