from rest_framework import viewsets, parsers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from milife_back.base import response
from . import models, serializers
from milife_back.users.models import User

import uuid

class DocumentsViewSet(viewsets.GenericViewSet):
    parsers = (parsers.FileUploadParser, )
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.filter(deleted=False)

    def list(self, request, user_pk):
        documents = self.queryset.filter(user = user_pk)
        serializer = self.get_serializer(documents, many=True)
        return response.Ok(serializer.data)

    def delete(self, request, pk, user_pk=None):
        pass

    def retrieve(self, request, user_pk, pk):
        document = self.queryset.get(id=pk)
        serializer = self.get_serializer(document)
        return response.Ok(serializer.data)

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


#class NestedDocumentViewSet(NestedHyperlinkedModelSerializer):

