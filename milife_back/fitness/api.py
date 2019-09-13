from rest_framework.views import APIView
from rest_framework import viewsets, parsers, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend


from milife_back.base import response, mixins
from milife_back.permissions import NestedUserPermission
from . import models, serializers
from django.contrib.auth import get_user_model

from rest_framework_bulk import (
    BulkModelViewSet,
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)

import uuid


class NestedUserQuerysetMixin(object):
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
            return self.queryset.filter(user=str(user_pk))
        return self.queryset

class NestedProgrammeQuerysetMixin(object):
    def get_queryset(self):
        pk = self.kwargs.get('programme_pk')
        if pk:
            return self.queryset.filter(programme=str(pk))
        return self.queryset


class BulkWeightViewSet(BulkModelViewSet):
    queryset = models.Weight.objects.all()
    serializer_class = serializers.BulkWeightSerializer
    permission_classes = (IsAdminUser, )

class BulkTargetWeightViewSet(BulkModelViewSet):
    queryset = models.TargetWeight.objects.all()
    serializer_class = serializers.BulkTargetWeightSerializer
    permission_classes = (IsAdminUser, )


class WeightViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.WeightSerializer
    queryset = models.Weight.objects.all()
    permission_classes = (NestedUserPermission,)

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        user = get_user_model().objects.get(id=user_pk)
        context = {
            'user_ref': user,
        }
        super_context.update(context)
        return super_context


class TargetWeightViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.TargetWeightSerializer
    queryset = models.TargetWeight.objects.all()
    permission_classes = (NestedUserPermission,)

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        user = get_user_model().objects.get(id=user_pk)
        context = {
            'user_ref': user
        }
        super_context.update(context)
        return super_context


class ProgrammeViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ProgrammeSerializer
    queryset = models.Programme.objects.all()
    permission_classes = ()


class HolidayViewSet(NestedProgrammeQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.HolidaySerializer
    queryset = models.Holiday.objects.all()
    permission_classes = ()


class SessionLedgerViewSet(NestedProgrammeQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.SessionLedgerSerializer
    queryset = models.SessionLedger.objects.all()
    permission_classes = ()


from rest_framework import generics
from django_filters import rest_framework as drf_filters
from django.core.validators import EMPTY_VALUES

class EmptyStringFilter(drf_filters.BooleanFilter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        exclude = self.exclude ^ (value is False)
        method = qs.exclude if exclude else qs.filter

        return method(**{self.field_name: ""})

class MessageFilter(drf_filters.FilterSet):
    content_isempty = EmptyStringFilter(field_name="content")

    class Meta:
        model = models.Message
        fields = ['kind', 'read', 'deleted',]


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MessageSerializer
    queryset = models.Message.objects.all()
    #permission_classes = (NestedUserPermission,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ('content' )
    ordering_fields = ('created_at', )
    # filterset_fields = ('kind', 'read', 'deleted',)
    filter_class = MessageFilter

    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
            return self.queryset.filter(recipient=str(user_pk))
        return self.queryset

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        user = get_user_model().objects.get(id=user_pk)
        context = {
            'recipient': user,
            "sender": self.request.user
        }
        super_context.update(context)
        return super_context


class MealPlanViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.MealPlanSerializer
    queryset = models.MealPlan.objects.all()
    permission_classes = (NestedUserPermission, )

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        user = get_user_model().objects.get(id=user_pk)
        context = {
            'user_ref': user,
        }
        super_context.update(context)
        return super_context


class CheckinViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    parsers = (parsers.FileUploadParser, )
    serializer_class = serializers.CheckinSerializer
    queryset = models.Checkin.objects.all()
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('date_of_checkin', )
    lookup_field = "date_of_checkin"


    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        client = get_user_model().objects.get(id=user_pk)
        context = {
            'user': client
        }
        super_context.update(context)
        return super_context


class ClientDashboardViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.ClientDashboardSerializer
    permission_classes = (AllowAny, )

    def retrieve(self, *args, **kwargs):
        user_pk = self.kwargs['pk']
        client = get_user_model().objects.get(id=user_pk)
        weight_queryset = models.Weight.objects.filter(user=client)
        messages_count = models.Message.objects.filter(recipient=client, read=False).exclude(content='').count()
        first_checkin = models.Checkin.objects.filter(user=client).order_by('date_of_checkin')[0]
        try:
            meal_plan = models.MealPlan.objects.get(user=client)
        except models.MealPlan.DoesNotExist:
            calorie = 0
        else:
            calorie = meal_plan.calorie

        try:
            programme = models.Programme.objects.filter(user=client).order_by('-start_date')[:1][0]
        except IndexError:
            programme = None

        context = {
            "weight_log": list(weight_queryset),
            "target_weight": models.TargetWeight.objects.filter(user=client),
            "progress_report": models.Checkin.objects.filter(user=client).order_by('-date_of_checkin')[:2],
            "calorie": calorie,
            "messages_count": messages_count,
            "programme": programme,
            "first_checkin": first_checkin
        }
        serializer = self.serializer_class(instance=context)
        return response.Ok(serializer.data)


class WeightChartViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.WeightChartSerializer
    permission_classes = (AllowAny, )

    def list(self, *args, **kwargs):
        user_pk = self.kwargs['user_pk']
        client = get_user_model().objects.get(id=user_pk)
        weight_queryset = models.Weight.objects.filter(user=client)

        context = {
            "weight_log": list(weight_queryset),
            "target_weight": models.TargetWeight.objects.filter(user=client),
        }
        serializer = self.serializer_class(instance=context)
        return response.Ok(serializer.data)


class ProgressReportViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ProgressReportDetailSerializer
    queryset = models.Checkin.objects.all()
    permission_classes = (NestedUserPermission, )
    lookup_field = "date_of_checkin"
    http_method_names = ['get', 'head']

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        client = get_user_model().objects.get(id=user_pk)
        context = {
            'user': client
        }
        super_context.update(context)
        return super_context


class AccuniqDataViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AccuniqDataSerializer
    queryset = models.AccuniqData.objects.all()
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ('created_at', )
    permission_classes = (IsAdminUser, )

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        # user_pk = self.kwargs['user_pk']
        # client = get_user_model().objects.get(id=user_pk)
        context = {
            'uploaded_by': self.request.user
        }
        super_context.update(context)
        return super_context
