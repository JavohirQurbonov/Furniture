from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'phone',
            'first_name',
            'age',
            'address',
        ]
        read_only_fields = ('id','phone')

class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    code = serializers.CharField(max_length=6)

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=13)
    code = serializers.CharField(max_length=6)
    first_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=14,max_value=120)
    address = serializers.CharField()

