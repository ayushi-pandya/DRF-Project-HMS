from datetime import datetime

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from appointment.models import Appointments, Room, Admit, AdmitStaff, Notification
from appointment.serializers import AddAppointmentSerializer, LoadTimeslotsSerializer, ViewAppointmentSerializer, \
    AddRoomSerializer, AdmitPatientSerializer, DischargeByDoctorSerializer
from users.models import Staff, Patient
from users.renderers import UserRenderer


class LoadTimeslots(APIView):
    """
    API for give data to ajax call for loading available  timeslots  from database
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
    """
    API for adding rooms data
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Room.objects.all()
    serializer_class = AddRoomSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'msg': 'Room Created successfully'}, status=status.HTTP_201_CREATED)


class SearchRoom(APIView):
    """
    API for give data to ajax call for search rooms
    """

    def get(self, request):
        room = Room.objects.all().values_list('room_type', flat=True)
        room_list = list(room)
        return Response(room_list, status=status.HTTP_201_CREATED)


class ViewRooms(generics.ListAPIView):
    """
    API for showing list of appointments
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = AddRoomSerializer

    def get_queryset(self):
        queryset = Room.objects.all()
        return queryset


class AdmitPatientView(generics.CreateAPIView):
    """
    API for adding rooms data
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):

        serializer = AdmitPatientSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            fetch_room = request.data.get('room')
            fetch_patient = request.data.get('patient')
            fetch_staff = request.data.get('staff')
            fetch_disease = request.data.get('disease')
            fetch_in_date = request.data.get('in_date')

            get_room = Room.objects.get(id=fetch_room)
            get_patient = Patient.objects.get(id=fetch_patient)
            admit_patient = Admit.objects.create(room=get_room, patient=get_patient, disease=fetch_disease,
                                                 in_date=fetch_in_date)

            if len(fetch_staff) > 1:
                for i in range(len(fetch_staff)):
                    get_staff = Staff.objects.filter(id=fetch_staff[i]).first()
                    admit_patient.staff.add(get_staff)
            else:
                get_staff = Staff.objects.filter(id=fetch_staff)
                admit_patient.staff.add(get_staff)

            return Response({'msg': 'Patient Admitted successfully'}, status=status.HTTP_201_CREATED)


class ViewAdmitPatient(generics.ListAPIView):
    """
    API for showing list of admitted patient
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = AdmitPatientSerializer

    def get_queryset(self):
        queryset = Admit.objects.filter(out_date__isnull=True)
        return queryset


class SearchAdmitPatient(APIView):
    """
    API for give data to ajax call for search admit user
    """

    def get(self, request):
        patient = Admit.objects.all().values_list('patient__patient__username', flat=True)
        return Response(list(patient), status=status.HTTP_200_OK)


class DischargeByDoctor(generics.CreateAPIView):
    """
    saving discharge request in notification module
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Notification.objects.all()
    serializer_class = DischargeByDoctorSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'msg': 'Patient Discharged by Doctor successfully'}, status=status.HTTP_201_CREATED)
