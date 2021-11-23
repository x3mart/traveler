from modeltranslation.manager import get_translatable_fields_for_model
from rest_framework import serializers
from modeltranslation.utils import get_language


def get_translatable_fields_source(self):
    print(get_translatable_fields_for_model(self.Meta.model))
    if get_translatable_fields_for_model(self.Meta.model):
        actualy_translatable_fields = list(set(get_translatable_fields_for_model(self.Meta.model)).intersection(self.fields))
        for field in actualy_translatable_fields:
            self.fields[field] = serializers.CharField(required=False, source=f"{field}_{get_language()}")
    return self.fields

class TranslatedModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = get_translatable_fields_source(self)