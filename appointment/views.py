from datetime import datetime

from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from appointment.models import Appointments
from appointment.serializers import AddAppointmentSerializer
from users.models import Staff


class LoadTimeslots(APIView):
    """
    class for give data to ajax call for loading available  timeslots  from database
    """

    def get(self, request):
        fetch_staff = request.data.get('staff')
        fetch_date = request.data.get('date')
        fetch_time = Appointments.objects.filter(staff_id=fetch_staff).filter(date=fetch_date)
        user_data = []
        time_slot_choices = []
        time_list = []
        for i in fetch_time:
            time_list.append(i.timeslot)
        time = datetime.now()
        date = datetime.now().date()
        current_time = time.strftime("%H:%M:%S")
        if str(fetch_date) == str(date):
            for i in range(9, 20):
                if i > int(current_time.split(':')[0]):
                    if i != 12:
                        user_data.append(i)
                        time_slot_choices.append(f"{i}:00")
        else:
            for i in range(9, 20):
                if i != 12:
                    user_data.append(i)
                    time_slot_choices.append(f"{i}:00")
        time_list = sorted(time_list)
        time_slot_choices = sorted(time_slot_choices)
        b = set(time_slot_choices).difference(time_list)
        b = list(sorted(b))
        return JsonResponse(b, safe=False)


class AddAppointmentView(generics.CreateAPIView):
    serializer_class = AddAppointmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'msg': 'Appointment Added successfully'}, status=status.HTTP_200_OK)

