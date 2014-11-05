from django.forms import widgets
from rest_framework import serializers
from passport.models import Timeslot, Boat, Assignment, Booking

class TimeslotSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='transform_id')
    class Meta:
        model = Timeslot
        fields = ('id', 'start_time', 'duration', 'availability', 'customer_count')
	

class BoatSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='transform_id')
    class Meta:
	model = Boat
        fields = ('id', 'name', 'capacity')


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('timeslot', 'boat')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('timeslot', 'boat', 'size')
