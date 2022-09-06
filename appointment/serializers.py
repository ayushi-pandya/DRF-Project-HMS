from datetime import datetime

from rest_framework import serializers

from appointment.models import Appointments, Room
from users.models import Staff


class AddAppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for appointment
    """

    class Meta:
        model = Appointments
        fields = ['staff', 'date', 'timeslot', 'disease']

    def validate(self, attrs):
        staff = attrs.get('staff')
        date = attrs.get('date')
        timeslot = attrs.get('timeslot')
        fetch_staff = Staff.objects.filter(id=staff.id).filter(is_approve=True).filter(is_available=True).first()
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().date()
        if date == current_date and int(timeslot.split(':')[0]) <= int(current_time.split(':')[0]):
            raise serializers.ValidationError('This time is past you can not choose this time')
        if not fetch_staff:
            raise serializers.ValidationError('This staff is not available')
        if 9 < int(timeslot.split(':')[0]) > 18:
            raise serializers.ValidationError('Hospital timing is 9 to 6 please choose time in between that.')
        user = Appointments.objects.filter(staff=fetch_staff.id).filter(date=date).filter(timeslot=timeslot)
        if user:
            raise serializers.ValidationError('This slot is already been booked..Please choose another slot')
        return attrs


class LoadTimeslotsSerializer(serializers.ModelSerializer):
    """
    serializer for loading timeslots
    """

    class Meta:
        model = Appointments
        fields = ['staff', 'date']

    def validate(self, attrs):
        fetch_staff = attrs.get('staff')
        staff = Staff.objects.filter(id=fetch_staff.id).filter(is_approve=True).filter(is_available=True)
        if not staff:
            raise serializers.ValidationError('This staff is not available')
        return attrs


class ViewAppointmentSerializer(serializers.ModelSerializer):
    """
    serializer for appointment view
    """

    class Meta:
        model = Appointments
        fields = ['user', 'staff', 'date', 'timeslot', 'disease']


class AddRoomSerializer(serializers.ModelSerializer):
    """
    serializer for adding rooms
    """

    class Meta:
        model = Room
        fields = ['charge', 'AC', 'is_ICU', 'room_type']
