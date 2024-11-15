from rest_framework import serializers
from .models import Availability
from datetime import datetime, date

# Serializer For Availability Slot Booking
class AvailabilitySerializer(serializers.ModelSerializer):
    user_id         = serializers.ReadOnlyField(source = 'user.id')
    username        = serializers.ReadOnlyField(source = 'user.username')
    booked_id       = serializers.ReadOnlyField(source = 'id')
    user_type       = serializers.SerializerMethodField()


    class Meta:
        model               = Availability
        fields              = ['user_id','username','user_type','booked_id','available_date', 
                               'available_time_from', 'available_time_to']
        read_only_fields    = ['user_id']

    # Function to get user type date into user_type variable
    def get_user_type(self, obj):
        '''
        Function to find the type of user who has booked the slot
        '''
        user    = obj.user

        if user.is_superuser:
            return 'HR'
        elif user.is_staff and not user.is_superuser:
            return 'Interviewer'
        elif user.is_active and not user.is_staff and not user.is_superuser:
            return 'Candidate'
        return 'Unknown'
    
    def time_to_seconds(self, time_data):
        '''
        Function to convert the time that is in hour, minutes and seconds into seconds
        '''
        return time_data.hour * 3600 + time_data.minute *60 + time_data.second

    def validate(self, data):
        '''
        Function to Validate and return error messages if any.
        '''
        user                        = self.context['request'].user

        # User entered availability date
        available_date              = data['available_date']

        # User entered availability time
        available_time_from         = data['available_time_from']
        available_time_to           = data['available_time_to']

        # Converting the time to seconds
        available_from_seconds      = self.time_to_seconds(available_time_from)
        available_to_seconds        = self.time_to_seconds(available_time_to)

        # Checking for any overlapping time slots
        overlapping_slots = Availability.objects.filter( user = user, available_date = available_date, 
                                                        available_time_from__lt = available_time_to,
                                                        available_time_to__gt = available_time_from)

        if overlapping_slots.exists():
            raise serializers.ValidationError("You have already booked a slot on this time frame")
        
        # Validation for greater from time that to time
        if data['available_time_from'] >= data['available_time_to']:
            raise serializers.ValidationError("The 'available time from' should be before 'available time to' ")

        # Validation for older dates
        if data['available_date'] < date.today():
            raise serializers.ValidationError("Select a date that is today or in the future")
        
        # Validation for older from time
        if data['available_time_from'] < datetime.now().time() and data['available_date'] == date.today():
            raise serializers.ValidationError("Select a time that is now or in the future")

        # Validation for 1 hour not availability in slot
        if available_to_seconds - available_from_seconds < 3600:
            raise serializers.ValidationError("Interview requires at least 1 Hour of time")

        return data



class SchedulableTimeSerializer(serializers.Serializer):
    candidate_id        = serializers.IntegerField(required = True)
    hr_id               = serializers.IntegerField(required = True)