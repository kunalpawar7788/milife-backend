from rest_framework import viewsets, parsers, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from milife_back.base import response, mixins
from . import models, serializers
from milife_back.users.models import User

import uuid


class DocumentsViewSet(mixins.NestedQuerysetMixin, viewsets.ModelViewSet):
    parsers = (parsers.FileUploadParser, )
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.filter(deleted=False)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name', 'notes')
    filterset_fields = ('kind',)


    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        client = get_user_model().objects.get(id=user_pk)

        context = {
            'user': client,
            'uploaded_by': self.request.user,
        }
        super_context.update(context)
        return super_context
