from rest_framework import viewsets, parsers, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from milife_back.base import response, mixins
from . import models, serializers
from milife_back.users.models import User

import uuid


class DocumentsViewSet(mixins.NestedQuerysetMixin, viewsets.ModelViewSet):
    parsers = (parsers.FileUploadParser, )
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.filter(deleted=False)
    search_fields = ('name', 'notes')
    filter_backends = (filters.SearchFilter,)

    @permission_classes((IsAdminUser,))
    def create(self, request, user_pk=None):
        user = User.objects.get(id=user_pk)
        data = {
            'user': uuid.UUID(str(user.id)),
            'document': request.data['document'],
            'uploaded_by': uuid.UUID(str(request.user.id)),
            'name': request.data['name']
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return response.Created()

