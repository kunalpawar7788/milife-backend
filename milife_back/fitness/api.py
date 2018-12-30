from rest_framework import viewsets, parsers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from milife_back.base import response
from . import models, serializers
from milife_back.users.models import User

import uuid

class WeightViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.WeightSerializer
    queryset = models.Weight.objects.all()

    def list(self, request, user_pk=None):
        user_pk = user_pk or request.user.id
        instances = self.queryset.filter(user=user_pk)
        serializer = self.get_serializer(instances, many=True)
        return response.Ok(serializer.data)

    def delete(self, request, pk, user_pk=None):
        pass

    def retrieve(self, request, pk, user_pk=None):
        pass
