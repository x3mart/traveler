from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from languages.models import Language
from languages.serializers import LanguageSerializer, LanguagesSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all().order_by('name')
    serializer_class = LanguageSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class LanguageView(generics.CreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguagesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=400)
        languages = []
        for language in data['language']:
            languages.append(Language(**language))
        Language.objects.bulk_create(languages)
        return Response({}, status=200)