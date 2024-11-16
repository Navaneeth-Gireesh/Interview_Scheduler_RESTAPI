from django.urls import path, include
from .views import RegisterTimeSlotsView, AccountRegistrationView, SchedulableTimeView
from rest_framework.routers import DefaultRouter
from . import views

# Routers Setting
router = DefaultRouter()

router.register(r'Register_Slots', RegisterTimeSlotsView, basename='Register_Slots')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('account_registration',AccountRegistrationView.as_view() ,name = 'account_registration'),
    path('Schedulable_Slots', SchedulableTimeView.as_view(), name='Schedulable_Slots')

]

