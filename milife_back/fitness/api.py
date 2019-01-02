from rest_framework import viewsets, parsers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from milife_back.base import response
from milife_back.permissions import NestedUserPermission
from . import models, serializers
from milife_back.users.models import User

import uuid

class NestedQuerysetMixin(object):
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
            return self.queryset.filter(user=str(user_pk))
        return self.queryset

    
class WeightViewSet(NestedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.WeightSerializer
    queryset = models.Weight.objects.all()
    permission_classes = (NestedUserPermission,)


class ProgrammeViewSet(NestedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ProgrammeSerializer
    permission_classes = ()


class MessageViewSet(NestedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.MessageSerializer
    permission_classes = ()


class MealPlanViewSet(NestedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.MealPlanSerializer
    permission_classes = ()


class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SessionSerializer
