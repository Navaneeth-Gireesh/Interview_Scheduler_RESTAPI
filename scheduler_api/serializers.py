from rest_framework import serializers
from .models import Availability
from django.contrib.auth.models import User
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
        # Validation if already same timing slot is created
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
    interviewer_id       = serializers.IntegerField(required = True)


# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, style = {'input_type' : 'password'})
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        '''
        Function to check if an account with the same email exists
        '''
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        '''
        Function to check if an account with the same username exists
        '''
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

        
    def create(self, validated_data):
        user = User.objects.create(
            username    = validated_data['username'],
            email       = validated_data['email'],
                
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



