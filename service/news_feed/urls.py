from .views import UserViewSet, ArticleViewSet\
    # , NewsFeedViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=False)
router.register(r'user', UserViewSet, basename='user')
router.register(r'article', ArticleViewSet, basename='article')
# router.register(r'', NewsFeedViewSet, basename='')

urlpatterns = router.urls
