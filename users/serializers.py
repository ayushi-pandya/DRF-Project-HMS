from xml.dom import ValidationErr

from rest_framework import serializers

from users import models
from users.models import User, UserRole, StaffSpeciality, Staff, Medicine, Prescription, PrescribeMedicine, Emergency
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
        role = attrs.get('role')
        fetch_role = UserRole.objects.filter(role=role)
        if fetch_role:
            raise serializers.ValidationError('This role is already been added')
        return attrs


class AddStaffSpecialitySerializer(serializers.ModelSerializer):
    """
    Serializer for adding the staff speciality
    """

    class Meta:
        model = StaffSpeciality
        fields = ['speciality']

    def validate(self, attrs):
        speciality = attrs.get('speciality')
        fetch_speciality = StaffSpeciality.objects.filter(speciality=speciality)
        if fetch_speciality:
            raise serializers.ValidationError('This speciality is already been added')
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user update
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'age', 'address', 'profile']


class StaffUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for user update
    """

    class Meta:
        model = Staff
        fields = ['salary', 'is_approve', 'is_available', 'speciality']

    def validate(self, attrs):
        user = self.context.get('user')
        fetch_user = User.objects.get(id=user.staff_id)
        speciality = attrs.get('speciality')
        if str(fetch_user.role) == 'Nurse' and str(speciality) != 'Nurse':
            raise serializers.ValidationError('You are Nurse you can not choose another role')
        return attrs


class ViewStaffSerializer(serializers.ModelSerializer):
    """
    Serializer for showing list of staff
    """

    class Meta:
        model = Staff
        fields = ['staff', 'salary', 'is_approve', 'is_available', 'speciality']


class AddMedicineSerializer(serializers.ModelSerializer):
    """
    Serializer for adding medicines
    """

    class Meta:
        model = Medicine
        fields = ['medicine_name', 'charge']

    def validate(self, attrs):
        medicine_name = attrs.get('medicine_name')
        charge = attrs.get('charge')
        charge = str(charge)
        fetch_medicine = Medicine.objects.filter(medicine_name=medicine_name)
        if len(fetch_medicine) != 0:
            raise serializers.ValidationError('This medicine is already been added')
        if int(charge.split('.')[0]) <= 1:
            raise serializers.ValidationError('Medicine cost can not be zero')
        return attrs


class MedicineCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescribeMedicine
        fields = ['medicine', 'count']


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for patient prescription
    """
    medicines = MedicineCountSerializer(source='medicine', many=True, write_only=True)

    # count = serializers.IntegerField(source='medicine.count')

    class Meta:
        model = Prescription
        fields = ['patient', 'staff', 'medicines']

    # def create(self, validated_data):
    # line_items = validated_data.pop('medicine')
    # print(line_items)
    # instance = super(PrescriptionSerializer, self).create(validated_data)
    # print(instance)
    # for item in line_items:
    #     print(1)
    #     instance.count.add(item['count'])
    #
    #     # m = instance.medicine.add(item['medicine'])
    #     print(2)
    #     print(m,'///')
    # instance.save()
    # return instance
    # m = validated_data.get('medicine')
    # dish_item = validated_data["medicine"]
    # print(dish_item)
    # item_obj = models.PrescribeMedicine.objects.create(**dish_item)
    #
    # validated_data["medicines"] = item_obj
    # return super().create(validated_data)


class EmergencyCaseSerializer(serializers.ModelSerializer):
    """
    Serializer for emergency case
    """

    class Meta:
        model = Emergency
        fields = ['patient', 'staff', 'disease', 'charge']

    def validate(self, attrs):
        staff = attrs.get('staff')
        charge = attrs.get('charge')
        charge = str(charge)
        get_staff = Staff.objects.filter(id=staff.id).filter(is_available=True).filter(is_approve=True)
        if len(get_staff) == 0:
            raise serializers.ValidationError("This staff is not available")
        if int(charge.split('.')[0]) <= 1:
            raise serializers.ValidationError('Charge can not be zero')
        return attrs


class ViewEmergencyCaseSerializer(serializers.ModelSerializer):
    """
    Serializer for emergency case
    """

    class Meta:
        model = Emergency
        fields = ['patient', 'staff', 'datetime', 'disease', 'charge']


class ViewMedicineSerializer(serializers.ModelSerializer):
    """
    Serializer for view medicines
    """

    class Meta:
        model = Medicine
        fields = ['medicine_name', 'charge']
