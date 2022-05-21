from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    model = Article
    fields = '__all__'