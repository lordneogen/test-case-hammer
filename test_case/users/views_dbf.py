from django.http import JsonResponse
from rest_framework import generics
from . import serializers
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def C_Users(request):

    ser = serializers.SER_Users_C_1(data=request.data)

    if ser.is_valid():
            ser.save()
    return Response(ser.data)