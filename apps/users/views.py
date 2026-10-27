from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from apps.users.serializers import UserSerializer, SendOTPSerializer, VerifyOTPSerializer, RegisterSerializer
from apps.users.services import send_otp, verify_otp


# Create your views here.

def tokens_for_user(user)->dict:
    refresh = RefreshToken.for_user(user)
    return {
        'access':str(refresh.access_token),
        'refresh': str(refresh),
        'user':UserSerializer(user).data
    }

# class SendOTPView(APIView):
#     permission_classes = [AllowAny]
#     def post(self,request):
#         ser = SendOTPSerializer(data=request.data)
#         ser.is_valid(raise_exception=True)
#         phone = ser.validated_data['phone']
#         result = send_otp(phone)
#         return Response(result)

class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = SendOTPSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        result = send_otp(ser.validated_data['phone'])

        if result.get('ok') is False:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        ser = VerifyOTPSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        phone = ser.validated_data['phone']
        code = ser.validated_data['code']

        if not verify_otp(phone,code):
            return Response({'detail':'Kod noto\'g\'ri yoki muddati o\'tgan'},status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone = phone)
        except User.DoesNotExist:
            return Response({'detail':'Foydalanuvchi topilmadi.Avval ro\'yxatdan o\'ting!'},status=status.HTTP_404_NOT_FOUND)
        return Response(tokens_for_user(user))

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        if not verify_otp(data['phone'],data['code']):
            return Response({'detail':'Kod noto\'g\'ri yoki muddati o\'tgan!!!'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone = data['phone']).exists():
            return Response({'detail':'Bu telefon raqam allaqachon ro\'yxatdan o\'tgan!!!'},status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            first_name = data['first_name'],
            age = data['age'],
            phone = data['phone'],
            address = data['address']
        )
        return Response(tokens_for_user(user),status=status.HTTP_201_CREATED)

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response(UserSerializer(request.user).data)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response(UserSerializer(request.user).data)

    def patch(self,request):
        ser = UserSerializer(request.user,data=request.data,partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

