from datetime import datetime
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from appointment.models import Appointments, Room
from appointment.serializers import AddAppointmentSerializer, LoadTimeslotsSerializer, ViewAppointmentSerializer, \
    AddRoomSerializer
from users.renderers import UserRenderer


class LoadTimeslots(APIView):
    """
    class for give data to ajax call for loading available  timeslots  from database
    """

    def get(self, request):
        serializer = LoadTimeslotsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fetch_staff = serializer.data.get('staff')
        fetch_date = serializer.data.get('date')
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
        available_time = set(time_slot_choices).difference(time_list)
        return Response(list(sorted(available_time)), status=status.HTTP_200_OK)


class AddAppointmentView(generics.CreateAPIView):
    """
    API for adding appointment
    """
    serializer_class = AddAppointmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'msg': 'Appointment Added successfully'}, status=status.HTTP_200_OK)


class ViewAppointment(generics.ListAPIView):
    """
    API for showing list of appointments
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    serializer_class = ViewAppointmentSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            queryset = Appointments.objects.all()
        else:
            queryset = Appointments.objects.filter(user=self.request.user)
        return queryset


class DeleteAppointmentView(APIView):
    """
    API for deleting appointment
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        fetch_id = pk
        fetch_user = get_object_or_404(Appointments, pk=fetch_id)
        fetch_user.delete()
        return Response({'msg': 'Appointment Deleted successfully'})


class AddRoomView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Room.objects.all()
    serializer_class = AddRoomSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'msg': 'Room Created successfully'}, status=status.HTTP_201_CREATED)
