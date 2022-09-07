from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView

from users.models import User, Staff
from users.renderers import UserRenderer
from users.serializers import UserLoginSerializer, UserRegistrationSerializer, UserProfileSerializer, \
    UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, AddUserRoleSerializer, \
    AddStaffSpecialitySerializer, UserUpdateSerializer, StaffUpdateSerializer
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
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddUserRoleSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Role Added successfully'}, status=status.HTTP_200_OK)


class AddStaffSpecialityView(APIView):
    """
    API for adding staff speciality
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AddStaffSpecialitySerializer(data=request.data, context={'user': request.user})
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
