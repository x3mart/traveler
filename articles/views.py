from rest_framework.viewsets import ReadOnlyModelViewSet

from articles.serializers import ArticleSerializer
from .models import Article

# Create your views here.
class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.filter(is_active=True)
    serializer_class = ArticleSerializer
    lookup_field = 'slug'