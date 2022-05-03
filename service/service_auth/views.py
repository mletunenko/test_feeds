from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from news_feed.views import ArticleViewSet
from django.contrib.auth import authenticate, login, logout


# Create your views here.

@api_view(['POST'])
def login_view(request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return Response()
    else:
        data = {
            'response': 'Invalid login/password'
        }
        return Response(data)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response()
