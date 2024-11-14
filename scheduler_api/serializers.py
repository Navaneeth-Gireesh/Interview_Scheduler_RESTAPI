from rest_framework import serializers
from .models import Availability

class AvailabilitySerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source = 'user.id')
    class Meta:
        model = Availability
        fields = ['user_id','id','available_date', 'available_time_from', 'available_time_to']


class SchedulableTimeSerializer(serializers.Serializer):
    candidate_id = serializers.IntegerField(required = True)
    hr_id = serializers.IntegerField(required = True)