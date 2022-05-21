from rest_framework import serializers
from utils.images import get_tmb_image_uri
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    tmb_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
    
    def get_tmb_avatar(self, obj): 
        return get_tmb_image_uri(self, obj) 