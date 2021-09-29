from modeltranslation.manager import get_translatable_fields_for_model
from rest_framework import serializers


def get_translatable_fields_source(self):
    for field in get_translatable_fields_for_model(self.Meta.model):
        self.fields[field] = serializers.CharField(required=False, source=f"{field}_{self.context['language']}")
    return self.fields