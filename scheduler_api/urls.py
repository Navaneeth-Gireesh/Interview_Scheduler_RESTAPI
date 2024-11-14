from django.urls import path, include
from .views import RegisterTimeSlots # SchedulableTimeSlots
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Register_Slots', RegisterTimeSlots, basename = 'Register_Slots'),
# router.register(r'Schedulable_Slots', SchedulableTimeSlots, basename='Schedulable_Slots')
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls))
]
