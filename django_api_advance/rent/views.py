from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import APIException, AuthenticationFailed
from .authentication import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta
from django.db import IntegrityError
from account.models import AccountUser
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer
from otp.models import OTP
import uuid

class CustomUserAPIView(APIView):
    permission_classes = (AllowAny,)  # Tuple syntax for single permission class
    
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            date_of_birth_str = serializer.validated_data.get('date_of_birth')
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            today = datetime.today().date()
            age_limit_date = date_of_birth + timedelta(days=365 * 18)

            if today < age_limit_date:
                return Response({"error": "Users must be at least 18 years old to register."},
                                status=status.HTTP_400_BAD_REQUEST)

            username = serializer.validated_data.get('username')
            if len(username) < 7:
                return Response({"error": "Username must be at least 7 characters long."},
                                status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({"error": {"username": ["Username already exists."]}},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                user = serializer.save()

                AccountUser.objects.create()  # Unsure about the purpose of this line

                wallet_address = serializer.validated_data.get('wallet_address') or self.generate_wallet_address()
                serializer.validated_data['wallet_address'] = wallet_address

                token, _ = Token.objects.get_or_create(user=user)

                return Response({'message': 'Registration was successful'}, status=status.HTTP_200_OK)

            except IntegrityError as e:
                if 'username' in str(e):
                    return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'email' in str(e):
                    return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'password' in str(e):  # Syntax error here, not sure what should be returned
                    return Response({'error': 'Password error.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': "Account created successfully! An OTP to confirm your verification has been sent to your mail"},
                                    status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_wallet_address(self):
        unique_id = uuid.uuid4().hex
        return f"{unique_id[:10]}-{unique_id[10:16]}"

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({'error': 'Method not allowed for this endpoint.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        user = User.objects.filter(email=request.data['email']).first()

        if not user:
            raise APIException('Invalid credent!')

        if not user.check_password(request.data['password']):
            raise APIException('Invalid credentials!')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key='refreshToken', value=refresh_token, httponly=True)
        response.data = {
            'token': access_token
        }

        return response
    
class UserAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode('utf-8')
            id = decode_access_token(token)

            user = User.objects.filter(pk=id).first()

            return Response(UserSerializer(user).data)

        raise AuthenticationFailed('unauthenticated')


class RefreshAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })


class LogoutAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, _):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {
            'message': 'success'
        }
        return response


    
