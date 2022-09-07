from datetime import datetime

from rest_framework import serializers

from appointment.models import Appointments, Room, Admit, Notification
from users.models import Staff, Patient


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


class AdmitPatientSerializer(serializers.ModelSerializer):
    """
    serializer for adding admitted patient
    """

    class Meta:
        model = Admit
        fields = ['room', 'patient', 'staff', 'disease', 'in_date']

    def validate(self, attrs):
        room = attrs.get('room')
        staff = self.context.get('staff')
        if len(staff) > 1:
            for i in range(len(staff)):
                get_staff = Staff.objects.filter(id=staff[i]).filter(is_available=True).filter(is_approve=True)
                if len(get_staff) == 0:
                    raise serializers.ValidationError("This staff is not available")
        else:
            get_staff = Staff.objects.filter(id=staff).filter(is_available=True).filter(is_approve=True)
            if len(get_staff) == 0:
                raise serializers.ValidationError("This staff is not available")
        available_room = Admit.objects.filter(out_date__isnull=True).filter(room=room)
        if available_room:
            raise serializers.ValidationError("This room already have patient..please choose another")
        return attrs


class DischargeByDoctorSerializer(serializers.ModelSerializer):
    """
    serializer for discharge patient by doctor
    """

    class Meta:
        model = Notification
        fields = ['patient']

    def validate(self, attrs):
        patient = attrs.get('patient')
        get_patient = Patient.objects.get(id=patient.patient_id)
        already_discharged = Admit.objects.filter(patient=get_patient).filter(out_date__isnull=False)
        if already_discharged:
            raise serializers.ValidationError("This patient is already discharged")
        return attrs


class DischargeByAdminSerializer(serializers.ModelSerializer):
    """
    serializer for discharge patient by admin
    """

    class Meta:
        model = Admit
        fields = ['charge']

    def validate(self, attrs):
        charge = attrs.get('charge')
        if charge is not None:
            if int(charge) < 1000:
                raise serializers.ValidationError("Charge can not be less than 1000")
            return attrs
        else:
            raise serializers.ValidationError('charge is required field')
