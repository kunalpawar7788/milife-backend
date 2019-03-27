from rest_framework import serializers
from . import models


class DocumentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return models.Document.objects.create(
            user = self.context['user'],
            uploaded_by = self.context['uploaded_by'],
            **validated_data,
        )

    class Meta:
        model = models.Document
        exclude = ('user', 'uploaded_by')
