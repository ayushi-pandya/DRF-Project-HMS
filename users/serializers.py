from xml.dom import ValidationErr

from rest_framework import serializers
from users.models import User, UserRole, StaffSpeciality
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from users.utils import EmailSend


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'age', 'address', 'gender', 'role', 'profile', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # validate password and conform password in registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Password and Password Confirm does not match')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login
    """
    username = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'age', 'address', 'gender', 'role', 'profile']


class UserChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for user change password
    """
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password and Password Confirm does not match')
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    """
    Serializer for send reset password email
    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
            # print(link)
            # send email code
            body = 'Click Following Link to Reset Your Password ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email,
            }
            EmailSend.send_email(data)
            return attrs
        else:
            raise ValidationErr('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for creating serializer for password reset
    """
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')

            if password != password2:
                raise serializers.ValidationError('Password and Password Confirm does not match')

            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationErr('Token is not valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationErr('Token is not valid or Expired')


class AddUserRoleSerializer(serializers.ModelSerializer):
    """
    Serializer for adding the user role
    """

    class Meta:
        model = UserRole
        fields = ['role']

    def validate(self, attrs):
        user = self.context.get('user')
        if not user.is_admin:
            raise serializers.ValidationError('You are not Admin...You can not access this page')
        return attrs


class AddStaffSpecialitySerializer(serializers.ModelSerializer):
    """
    Serializer for adding the staff speciality
    """

    class Meta:
        model = StaffSpeciality
        fields = ['speciality']

    def validate(self, attrs):
        user = self.context.get('user')
        if not user.is_admin:
            raise serializers.ValidationError('You are not Admin...You can not access this page')
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user update
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'age', 'address', 'profile']
