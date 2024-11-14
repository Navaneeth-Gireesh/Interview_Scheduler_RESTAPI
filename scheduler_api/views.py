from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Availability
from .serializers import AvailabilitySerializer, SchedulableTimeSerializer
# Create your views here.

class RegisterTimeSlots(viewsets.ModelViewSet):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Availability.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        return super().perform_create(serializer)


# class SchedulableTimeSlots(viewsets.ModelViewSet):
#     permission_classes = [IsAdminUser]
#     serializer_class = SchedulableTimeSerializer

