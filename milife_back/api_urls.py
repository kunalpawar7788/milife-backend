# Third Party Stuff
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# milife-back Stuff
from milife_back.base.api.routers import SingletonRouter
from milife_back.users.api import CurrentUserViewSet, UsersViewSet, UserCountViewSet, CoachesViewSet
from milife_back.users.auth.api import AuthViewSet
from milife_back.documents.api import DocumentsViewSet
from milife_back.schedule.api import ScheduleViewSet
from milife_back.fitness.api import (
    ProgrammeViewSet, WeightViewSet, CheckinViewSet, HolidayViewSet,
    SessionLedgerViewSet, TargetWeightViewSet, MessageViewSet,
    MealPlanViewSet, ClientDashboardViewSet, ProgressReportViewSet,
)

default_router = DefaultRouter()
singleton_router = SingletonRouter()


# Register all the django rest framework viewsets below.
default_router.register('auth', AuthViewSet, base_name='auth')
singleton_router.register('me', CurrentUserViewSet, base_name='me')
default_router.register('counts', UserCountViewSet, base_name="usercounts")
default_router.register('dashboard', ClientDashboardViewSet, base_name="dashboard")

simple_router = routers.SimpleRouter(trailing_slash=False)
simple_router.register('users', UsersViewSet, base_name='users')
simple_router.register('coaches', CoachesViewSet, base_name='coaches')
simple_router.register('programmes', ProgrammeViewSet, base_name='programmes')


nested_user_router = routers.NestedSimpleRouter(simple_router, r'users', lookup='user')

nested_user_router.register('documents', DocumentsViewSet, base_name='user_documents')
nested_user_router.register('programmes', ProgrammeViewSet, base_name='user_programmes')
nested_user_router.register('schedule', ScheduleViewSet, base_name='user_schedule')
nested_user_router.register('weight', WeightViewSet, base_name='user_weight')
nested_user_router.register('target-weights', TargetWeightViewSet, base_name='user_weight')
nested_user_router.register('checkin', CheckinViewSet, base_name='user_checkin')
nested_user_router.register('message', MessageViewSet, base_name='user_message')
nested_user_router.register('mealplan', MealPlanViewSet, base_name='user_message')

nested_user_router.register('progress-report', ProgressReportViewSet, base_name="user_progress_report")

nested_programme_router2 = routers.NestedSimpleRouter(simple_router, r'programmes', lookup='programme')
nested_programme_router2.register('holiday', HolidayViewSet, base_name="programme_holiday")
nested_programme_router2.register('session-ledger', SessionLedgerViewSet, base_name='programme_session_ledger')

nested_programme_router = routers.NestedSimpleRouter(nested_user_router, r'programmes', lookup='programme')
nested_programme_router.register('holiday', HolidayViewSet, base_name="programme_holiday")
nested_programme_router.register('session-ledger', SessionLedgerViewSet, base_name='programme_session_ledger')


default_router.register('schedule', ScheduleViewSet, base_name='schedule')
default_router.register('weight', WeightViewSet, base_name='weight')


# nested_simple_router = router.NestedSimpleRouter(trailing_slash=False)
# default_router.register('users/{pk}/documents', DocumentsViewSet, base_name="user_documents")6
# simple_router.register('users', UsersViewSet, base_name="users")
# default_router.register('documents', DocumentsViewSet, base_name="documents")
nested_user_router.register('weight', WeightViewSet, base_name='user_weight')


# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls + singleton_router.urls + simple_router.urls + nested_user_router.urls + nested_programme_router.urls + nested_programme_router2.urls

