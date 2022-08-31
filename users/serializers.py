from rest_framework import serializers
from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    create serializer for user registration
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
    create serializer for user login
    """
    username = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    create serializer for user profile
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'age', 'address', 'gender', 'role', 'profile']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    """
    create serializer for user change password
    """
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
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
