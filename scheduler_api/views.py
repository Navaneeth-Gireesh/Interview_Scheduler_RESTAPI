from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Availability
from .serializers import AvailabilitySerializer, UserRegistrationSerializer, SchedulableTimeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

# Create your views here.
class PaginationClass(PageNumberPagination):
    page_size               = 5

# Account Registration View 
class AccountRegistrationView(APIView):
    # Permission for all including non loggedin users
    permission_classes  = []
    http_method_names   = ['post']

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Register Time Slots View
class RegisterTimeSlotsView(viewsets.ModelViewSet):
    serializer_class        = AvailabilitySerializer
    permission_classes      = [IsAuthenticated]
    pagination_class        = PaginationClass
    search_fields           = ['user__username', 'available_date']
    filter_backends         = [DjangoFilterBackend, SearchFilter]
    filterset_fields        = ['available_date', 'user__is_staff']


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

        return Availability.objects.filter(
            Q(user=self.request.user) | # Loogedin user availability
            Q(user__is_staff=True) | # All Interviewer availability
            Q(user__is_superuser=True) # All HR availability
        )
        
    def get_http_method_names(self):

        user = self.request.user

        # If the user is a superuser (HR) or staff (Interviewer), allow 'GET' and 'POST'
        if user.is_superuser or user.is_staff:
            return ['GET', 'POST']

        # For other users, allow only 'POST'
        return ['POST']

    
    # Every time saving a booking of slot save it with current user as user data(Overriding the new object creation)
    def perform_create(self, serializer):
        
        serializer.save(user = self.request.user)
        return super().perform_create(serializer)
    

# Schedule Time Check (Access only to HR)
class SchedulableTimeView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):

        serializer = SchedulableTimeSerializer(data=request.data)

        if serializer.is_valid():
            candidate_id = serializer.validated_data['candidate_id']
            interviewer_id = serializer.validated_data['interviewer_id']

            candidate = get_object_or_404(User, id=candidate_id)
            interviewer = get_object_or_404(User, id=interviewer_id)

            # Ensuring candidate and interviewer have appropriate roles
            if not (candidate.is_active and not candidate.is_staff and not candidate.is_superuser):
                return Response({"error": "Invalid candidate role."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not (interviewer.is_active and interviewer.is_staff):
                return Response({"error": "Invalid interviewer role."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetching availability
            candidate_availability = Availability.objects.filter(user=candidate)
            interviewer_availability = Availability.objects.filter(user=interviewer)

            # If there is no availability 
            if not candidate_availability.exists():
                return Response({"error": "Candidate has no availability."}, status=status.HTTP_404_NOT_FOUND)
            
            if not interviewer_availability.exists():
                return Response({"error": "Interviewer has no availability."}, status=status.HTTP_404_NOT_FOUND)

            interview_slots = []

            # Loop through candidate availability and find matches
            for candidate_slot in candidate_availability:
                for interviewer_slot in interviewer_availability:

                    if candidate_slot.available_date != interviewer_slot.available_date:
                        continue

                    # Check for past dates
                    today = datetime.now().date()
                    if candidate_slot.available_date < today:
                        continue

                    # Find overlapping times
                    overlap_start = max(candidate_slot.available_time_from, interviewer_slot.available_time_from)
                    overlap_end = min(candidate_slot.available_time_to, interviewer_slot.available_time_to)

                    # Check if there is a valid overlap
                    if overlap_start >= overlap_end:
                        continue  

                    # Create 1-hour slots within the overlap period
                    overlap_start_dt = datetime.combine(candidate_slot.available_date, overlap_start)
                    overlap_end_dt = datetime.combine(candidate_slot.available_date, overlap_end)

                    while overlap_start_dt < overlap_end_dt:

                        # Add the valid slot to the list
                        interview_slots.append({
                            'date': candidate_slot.available_date,
                            'start_time': overlap_start_dt.time(),
                            'end_time': (overlap_start_dt+timedelta(hours=1)).time()
                        })
                        # Increase one hour from overlap start
                        overlap_start_dt += timedelta(hours=1)

            # Return the available slots if any are found
            if interview_slots:
                return Response(
                    {"schedulable_slots": interview_slots},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "No overlapping slots found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        # Handle invalid serializer data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

