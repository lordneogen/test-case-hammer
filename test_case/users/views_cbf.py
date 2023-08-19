# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import User
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import F
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class Auth(jwt_views.TokenObtainPairView):
    """_summary_

    Args:
        jwt_views (_type_): _description_

    Returns:
        _type_: _description_
    """
    

    serializer_class = serializers.AuthTokenSystem

    def post(self, request, *args, **kwargs):
        # Проверяем, есть ли пароль в запросе
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

#CLEAR 
def clear():
    """_summary_
    """
    necessary_time = timezone.now()- timezone.timedelta(minutes=1) # Отрегулируйте время по необходимости
    objects_to_delete = User.objects.filter(Q(auth_data__lt=necessary_time)).exclude( auth_code_1=F('auth_code_2'))
    print(objects_to_delete)
    objects_to_delete.delete()

#READ USERS
class R_Users(generics.ListAPIView, generics.RetrieveAPIView):
    """_summary_

    Args:
        generics (_type_): _description_
        generics (_type_): _description_

    Returns:
        _type_: _description_
    """

    authentication_classes = [JWTAuthentication, SessionAuthentication]  
    permission_classes = [IsAuthenticated]  



    queryset =  User.objects.all()
    serializer_class = serializers.SER_Users_R

    def list(self, *args, **kwargs):

        clear()

        queryset = User.objects.filter(referred_by=self.request.user)
        
        serializer = serializers.SER_Users_R(data=queryset, many=True)

        if serializer.is_valid():
            return Response({'error':'Нет пользователей'},status=404)

        res=serializer.data
        res.insert(0,{
                 "main_invite_code":self.request.user.invite_code
            })
        return Response(res)

#READ UPDATE DELETE USERS
class RUD_Users(generics.ListAPIView, generics.RetrieveAPIView):
    """_summary_

    Args:
        generics (_type_): _description_
        generics (_type_): _description_

    Returns:
        _type_: _description_
    """

    authentication_classes = [JWTAuthentication, SessionAuthentication] 
    permission_classes = [IsAuthenticated] 

    queryset =  User.objects.all()
    serializer_class = serializers.SER_Users_U


    def list(self, request, *args, **kwargs):

        clear()

        pk=kwargs.get('id')
        queryset = User.objects.filter(pk=pk)

        
        serializer = serializers.SER_Users_U(data=queryset, many=True)


        if ( serializer.is_valid() or len(queryset)==0 ) and pk:
            return Response({'error':'Нет пользователя'},status=404)
        if pk:
            return Response(serializer.data[0])
        else:
            res=serializer.data
            res.insert(0,{
                 "invite_code":request.user.invite_code
            })
            return Response(res)

    def put(self, request, *args, **kwargs):

        clear() 

        pk = kwargs.get('id')

        if not pk:
            return Response({'error':'Нет пользователя'},status=404)
        
        obj = User.objects.get(id=pk)

        ser = serializers.SER_Users_U(instance=obj, data=request.data,partial=True)


        if ser.is_valid():
            if not obj.referred_by:
                ser.save()
            else:
                ser.data['referred_by']=obj.referred_by
        return Response(ser.data)
    
    def delete(self, request, *args, **kwargs):

        clear()

        try:
            pk = kwargs.get('id')
            if not pk:
                return Response({'error': 'Нет пользователя'}, status=404)
        
            obj = User.objects.get(pk=pk)
            obj.delete()
            return Response({'message': 'Пользователь успешно удален'}, status=204)
        except:
            return Response({'error': 'Нет пользователя'}, status=404)
        # except User.DoesNotExist:
        #     return Response({'error': 'Пользователь не найден'}, status=404)
    
#CREATE USERS PART 1
class C_1_Users(generics.ListAPIView, generics.RetrieveAPIView):
    """_summary_

    Args:
        generics (_type_): _description_
        generics (_type_): _description_

    Returns:
        _type_: _description_
    """
    # authentication_classes = [JWTAuthentication, SessionAuthentication] 
    # permission_classes = [IsAuthenticated] 

    queryset =  {}
    serializer_class = serializers.SER_Users_C_1

    def post(self, request, *args, **kwargs):

        if User.objects.filter(phone_number=request.data["phone_number"]):
            return redirect('http://127.0.0.1:8000/users/login/')

        ser = serializers.SER_Users_C_1(data=request.data)
        
        if ser.is_valid():
            ser.save()

        print(ser.data)

        return redirect('access/{}'.format(ser.data['id']))

#CREATE USERS PART 2
class C_2_Users(generics.ListAPIView, generics.RetrieveAPIView):
    """AI is creating summary for C_2_Users

    Args:
        generics ([type]): [description]
        generics ([type]): [description]

    Returns:
        [type]: [description]
    """

    # authentication_classes = [JWTAuthentication, SessionAuthentication] 
    # permission_classes = [IsAuthenticated] 

    queryset =  {}
    serializer_class = serializers.SER_Users_C_2

    def put(self, request, *args, **kwargs):

        clear()

        pk = kwargs.get('id')
        if not pk:
            return Response({'error':'Нет пользователя'},status=404)
        obj = User.objects.get(id=pk)
        ser = serializers.SER_Users_C_2(instance=obj, data=request.data)
        if ser.is_valid():
            ser.save()
            
        return Response(ser.data)