from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
# Create your views here.

def homepage(request):
    context = {
        'homepage':"this my first page",
        }
    return render(request, 'penitansyeAPI/index.html',context)


# rest framework views
@api_view(['GET'])
def homeView(request):
    return Response({'message':"Welcome to my homepage"}, status=status.HTTP_200_OK)
