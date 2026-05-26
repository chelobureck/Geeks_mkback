import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer, RegisterSerializer, OTPRequestSerializer, OTPVerifySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['request_otp', 'verify_otp', 'register']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def request_otp(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                user.otp = otp
                user.save()
                
                send_mail(
                    'Your OTP Code',
                    f'Your verification code is: {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'OTP sent to email'})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email, otp=otp)
                user.otp = None  # Clear OTP after use
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'role': user.role})
            except User.DoesNotExist:
                return Response({'error': 'Invalid OTP or email'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
