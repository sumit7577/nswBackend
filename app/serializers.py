from django.forms import ValidationError
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from app.models import *
from django.contrib.auth.password_validation import validate_password
from app.views import totp
from django.db.models import Q



class UserDetailSerialzer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class OtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)



class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'password']

    def validate_email(self, value):
        if not is_email(value):
            raise serializers.ValidationError("Enter a valid email address. It should be in the format: 'example@domain.com'.")
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already registered.")
        return value

    def validate_phone(self, value):
        if not is_phone(value):
            raise serializers.ValidationError("Enter a valid phone number. This value must contain only 10 digits.")
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number already registered.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        password = validated_data.get('password')
        
        otp = totp.now()
        Otp.objects.filter(Q(phone=phone) | Q(email= email)).delete()
        if not Otp.objects.filter(otp=otp).exists():
            customer = Otp.objects.create(
                otp=otp, email=email, phone=phone, password=password
            )
            send_register_account_otp_mail(customer.email, otp)
        return validated_data  # Or return customer if you want to return the OTP object


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=200)
    password = serializers.CharField(required=True, max_length=128)


class SingleCourseSerializerPaid(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        depth=0


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields = ['id','name','image','description','content','starting_date','ending_date','teaching_time_start','teaching_time_end','registration_fees']


class PaidInstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = "__all__"
        depth = 0


class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = ['id','installment_number','date','price']



class OrderSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Order
        fields = ["id","order_data","status","payment_id","order_id","course","order_date"]