from rest_framework import serializers

from nurse.models import NurseDuty
from users.models import Staff


class AssignDutySerializer(serializers.ModelSerializer):
    """
    serializer for assigning duty to staff
    """

    class Meta:
        model = NurseDuty
        fields = ['staff', 'patient']

    def validate(self, attrs):
        staff = attrs.get('staff')
        get_staff = Staff.objects.filter(id=staff.id).filter(is_available=True).filter(is_approve=True)
        if len(get_staff) == 0:
            raise serializers.ValidationError("This staff is not available")
        return attrs
