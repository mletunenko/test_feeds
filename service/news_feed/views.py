from rest_framework.response import Response

from .serializers import UserSerializer, ArticleSerializer
# from rest_framework import status
# from rest_framework.decorators import action
from .models import User, Article
from rest_framework import viewsets, status
from django.db.models import Q


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_subscriber:
                user_id = request.user.id
                request = f'SELECT * FROM news_feed_article WHERE is_public=True ' \
                          f'OR author_id IN (SELECT to_user_id ' \
                          f'FROM news_feed_user_subscriptions WHERE ' \
                          f'from_user_id={user_id});'
                queryset = Article.objects.raw(request)
                serializer = ArticleSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.user.is_author:
                user_id = request.user.id
                queryset = Article.objects.filter(Q(is_public=True) | Q(author_id=user_id))
                serializer = ArticleSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            queryset = Article.objects.filter(is_public=True)
            serializer = ArticleSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


