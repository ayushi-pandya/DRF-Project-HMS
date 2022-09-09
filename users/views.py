from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from appointment.models import Appointments
from users.models import User, Staff, Patient, Medicine, Prescription, Emergency, PrescribeMedicine
from users.renderers import UserRenderer
from users.serializers import UserLoginSerializer, UserRegistrationSerializer, UserProfileSerializer, \
    UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, AddUserRoleSerializer, \
    AddStaffSpecialitySerializer, UserUpdateSerializer, StaffUpdateSerializer, ViewStaffSerializer, \
    AddMedicineSerializer, PrescriptionSerializer, EmergencyCaseSerializer, ViewEmergencyCaseSerializer, \
    ViewMedicineSerializer, ViewTodayAppointmentSerializer, ViewPrescriptionSerializer
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    generate jwt token manually
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    """
    API for user registration
    """
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API for user login
    """
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Username or password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    """
    API for display profile data of user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    """
    API for change password
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    """
    API for sending email to reset the password
    """
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send to your email successfully'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    """
    API for reset the password
    """
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, *args, **kwargs):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset successfully'}, status=status.HTTP_200_OK)


class AddUserRoleView(APIView):
    """
    API for adding user role
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = AddUserRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Role Added successfully'}, status=status.HTTP_200_OK)


class AddStaffSpecialityView(APIView):
    """
    API for adding staff speciality
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = AddStaffSpecialitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Speciality Added successfully'}, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    """
    API for updating user information
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        fetch_id = pk
        fetch_user = get_object_or_404(User, pk=fetch_id)
        serializer = UserUpdateSerializer(fetch_user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'User Updated successfully'}, status=status.HTTP_200_OK)


class UserDeleteView(APIView):
    """
    API for deleting user information
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        fetch_id = pk
        fetch_user = get_object_or_404(User, pk=fetch_id)
        fetch_user.delete()
        return Response({'msg': 'User Deleted successfully'})


class StaffUpdateView(generics.UpdateAPIView):
    """
    API for updating staff information
    """
    renderer_classes = [UserRenderer]
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'
    serializer_class = StaffUpdateSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        fetch_user = get_object_or_404(Staff, id=instance.id)
        serializer = StaffUpdateSerializer(instance, data=request.data, context={'user': fetch_user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Staff Updated successfully'}, status=status.HTTP_200_OK)


class SearchUser(APIView):
    """
    API for give data to ajax call for search user
    """

    def get(self, request):
        user = User.objects.all().values_list('username', flat=True)
        return Response(list(user), status=status.HTTP_200_OK)


class ViewUser(generics.ListAPIView):
    """
    API for showing list of user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class SearchStaff(APIView):
    """
    API for give data to ajax call for search user
    """

    def get(self, request):
        user = Staff.objects.all().values_list('staff__username', flat=True)
        return Response(list(user), status=status.HTTP_200_OK)


class ViewStaff(generics.ListAPIView):
    """
    API for showing list of staff
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = ViewStaffSerializer

    def get_queryset(self):
        queryset = Staff.objects.all()
        return queryset


class AddMedicineView(generics.CreateAPIView):
    """
    API for adding medicines
    """
    renderer_classes = [UserRenderer]
    serializer_class = AddMedicineSerializer

    def create(self, request, *args, **kwargs):
        print(self.request.user.role)
        if self.request.user.is_admin or str(self.request.user.role) == 'Doctor':
            super().create(request, *args, **kwargs)
            return Response({'msg': 'Medicine Added successfully'}, status=status.HTTP_201_CREATED)
        else:
            raise ValidationError('You have no rights to access this page')


class PrescriptionView(generics.CreateAPIView):
    """
    API for prescription of patient
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = PrescriptionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"requested_data": request.data['medicine']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': serializer.data, 'msg': 'LEAVE_CREATED'}, status=status.HTTP_201_CREATED)

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     print(1)
    #     print(self.request.user.role)
    #     print(2)
    #     if str(self.request.user.role) == 'Doctor':
    #         print(3)
    #         serializer = PrescriptionSerializer(data=request.data)
    #         if serializer.is_valid(raise_exception=ValueError):
    #             fetch_patient = request.data.get('patient')
    #             print('fetch_patient:', fetch_patient)
    #
    #             fetch_staff = request.data.get('staff')
    #             print('fetch_staff:', fetch_staff)
    #
    #             fetch_medicine = request.data.get('mediciness')
    #             print('fetch_medicine:', fetch_medicine)
    #
    #             get_patient = Patient.objects.get(id=fetch_patient)
    #             print('get_patient:', get_patient)
    #
    #             get_staff = Staff.objects.get(id=fetch_staff)
    #             print('get_staff:', get_staff)
    #
    #             prescribe_patient = Prescription.objects.create(patient=get_patient, staff=get_staff)
    #             print('prescribe_patient:', prescribe_patient)
    #
    #             for i in fetch_medicine:
    #                 print(i['medicine'])
    #                 print(i['count'])
    #
    #                 get_medicine = Medicine.objects.filter(id=i['medicine']).first()
    #                 print('get_medicine:', get_medicine)
    #
    #                 get_count = i['count']
    #
    #                 though_table_data = PrescribeMedicine.objects.create(prescription=prescribe_patient,
    #                                                                      medicine=get_medicine, count=get_count)
    #                 print(though_table_data)
    #             return Response({'msg': ' Prescription added successfully'}, status=status.HTTP_201_CREATED)
    #
    #             # fetch_count = request.data.get('count')
    #             # print('fetch_count:', fetch_count)
    #
    #
    #
    #             # if len(fetch_medicine) > 1 and len(fetch_count) > 1:
    #             #     for i in range(len(fetch_medicine)):
    #             #         print(4)
    #             #         get_medicine = Medicine.objects.filter(id=fetch_medicine[i]).first()
    #             #         print('get_medicine:', get_medicine)
    #             #         print(5)
    #             #         get_count = fetch_count[i]
    #             #         print('get_count:', get_count)
    #             #         print(6)
    #             #         though_table_data = PrescribeMedicine.objects.create(prescription=prescribe_patient,
    #             #                                                              medicine=get_medicine, count=get_count)
    #             #         print(though_table_data)
    #             #         # prescribe_patient.medicine.add(get_medicine)
    #             #         print(7)
    #             #         # prescribe_patient.count.add(get_count)
    #             #         # print(8)
    #             #         return Response({'msg': ' Prescription added successfully'}, status=status.HTTP_201_CREATED)
    #             #
    #             #
    #             # else:
    #             #     print(9)
    #             #     get_medicine = Medicine.objects.filter(id=fetch_medicine).first()
    #             #     print('get_medicine:', get_medicine)
    #             #     print(10)
    #             #     though_table_data = PrescribeMedicine.objects.create(prescription=prescribe_patient,
    #             #                                                          medicine=get_medicine, count=fetch_count)
    #             #     print(though_table_data)
    #             #     # prescribe_patient.medicine.add(get_medicine)
    #             #     # print(11)
    #             #     # prescribe_patient.count.add(fetch_count)
    #             #     print(12)
    #             #     return Response({'msg': ' Prescription added successfully'}, status=status.HTTP_201_CREATED)
    #
    #     # if str(request.user.role) == 'Doctor':
    #     #     super().create(request, *args, **kwargs)
    #     #     return Response({'msg': ' Prescription added successfully'}, status=status.HTTP_201_CREATED)
    #     # else:
    #     #     print(5)
    #     #     raise ValidationError('You have no rights to access this page')


class ViewPrescription(generics.ListAPIView):
    """
    API for showing list of prescription
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    serializer_class = ViewPrescriptionSerializer

    def get_queryset(self):
        print(self.request.user.id)
        if str(self.request.user.role) == 'Doctor':
            queryset = Prescription.objects.filter(staff=self.request.user.id)
            return queryset
        elif self.request.user.is_admin:
            queryset = Prescription.objects.all()
            return queryset
        else:
            raise ValidationError('You have no rights to access this page')


class EmergencyCaseView(generics.CreateAPIView):
    """
    API for emergency cases
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = EmergencyCaseSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'msg': 'Emergency Case Added successfully'}, status=status.HTTP_201_CREATED)


class SearchEmergency(APIView):
    """
    class for give data to ajax call for search user
    """

    def get(self, request):
        user = Emergency.objects.all().values_list('patient__patient__username', flat=True)
        return Response(list(user), status=status.HTTP_200_OK)


class ViewEmergency(generics.ListAPIView):
    """
    API for showing list of emergency cases
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = ViewEmergencyCaseSerializer

    def get_queryset(self):
        queryset = Emergency.objects.all()
        return queryset


class MedicineUpdateView(generics.UpdateAPIView):
    """
    API for updating medicine information
    """
    renderer_classes = [UserRenderer]
    queryset = Medicine.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'id'
    serializer_class = AddMedicineSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AddMedicineSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Medicine Updated successfully'}, status=status.HTTP_200_OK)


class SearchMedicine(APIView):
    """
    class for give data to ajax call for search medicine
    """

    def get(self, request):
        medicine = Medicine.objects.all().values_list('medicine_name', flat=True)
        return Response(list(medicine), status=status.HTTP_200_OK)


class ViewMedicine(generics.ListAPIView):
    """
    API for showing list of medicines
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = ViewMedicineSerializer

    def get_queryset(self):
        queryset = Medicine.objects.all()
        return queryset


class ViewTodayAppointment(generics.ListAPIView):
    """
    API for showing list today's appointment of a particular staff
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    serializer_class = ViewTodayAppointmentSerializer

    def get_queryset(self):
        if str(self.request.user.role) == 'Doctor' or str(self.request.user.role) == 'Nurse':
            get_staff = Staff.objects.filter(staff_id=self.request.user.id).filter(is_available=True).filter(
                is_approve=True)
            print(get_staff)
            if len(get_staff) == 0:
                raise ValidationError("You are not approved yet")
            else:
                date = datetime.now().date()
                queryset = Appointments.objects.filter(staff__staff__username=self.request.user).filter(
                    date=date).order_by('id')
                return queryset
        else:
            raise ValidationError('You have no rights to access this page')
