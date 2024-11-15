from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Availability
from .serializers import AvailabilitySerializer, SchedulableTimeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class PaginationClass(PageNumberPagination):
    page_size               = 5

class RegisterTimeSlots(viewsets.ModelViewSet):
    serializer_class        = AvailabilitySerializer
    permission_classes      = [IsAuthenticated]
    pagination_class        = PaginationClass
    search_fields           = ['user__username', 'available_date']
    filter_backends         = [DjangoFilterBackend, SearchFilter]
    filterset_fields        = ['available_date']

    def get_queryset(self):
        '''
        Function to show the query set data based on the role of the logged in user
        '''
        user = self.request.user

        # If superuser(HR) or staff(Interviewer)
        if user.is_superuser or user.is_staff:
            # Show all Booked Slots
            return Availability.objects.all()
        # else show only that particular users Bookings
        return Availability.objects.filter(user = self.request.user)
    
    # Every time saving a booking of slot save it with current user as user data(Overriding the new object creation)
    def perform_create(self, serializer):
        
        serializer.save(user = self.request.user)
        return super().perform_create(serializer)


# class SchedulableTimeSlots(viewsets.ModelViewSet):
#     permission_classes = [IsAdminUser]
#     serializer_class = SchedulableTimeSerializer

