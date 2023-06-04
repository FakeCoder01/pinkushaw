from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .models import Profile, User, OTPVerify, Preference, Question, Location, LeftSwipe
from .serializers import ProfileSerializer, UserSerializer, OTPVerificationSerializer


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404

import random

from google.oauth2 import id_token
from google.auth.transport.requests import Request


# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Profile.objects.get(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def profile_details(self, request, id=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=413)
    

    def update(self, request, id=None):
        queryset = Profile.objects.filter(user=self.request.user)
        profile = get_object_or_404(queryset, user=self.request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    def destroy(self, request, id=None):
        if id == None:
            id = request.data.get('id')
        queryset = Profile.objects.filter(user=self.request.user)
        profile = get_object_or_404(queryset, id=id)
        profile.delete()
        return Response(status=204)



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def set_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrf_token':csrf_token})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if request.data.get('confirm_password') != request.data.get('password'):
        return Response({'message': 'password not match'}, status=405)
    if serializer.is_valid():
        user = User.objects.create_user(
            username = request.data.get('username'),
            password = request.data.get('password'),
            email = request.data.get('username'),
            is_active = False    # set False if email auth is needed
        )
        preference = Preference.objects.create()
        question = Question.objects.create()
        location = Location.objects.create()
        profile = Profile.objects.create(
            user = user,
            location = location,
            question = question,
            preference = preference
        )
        left_swipe = LeftSwipe.objects.create(user=profile)
        email_code = random.randint(100000, 999999)
        otp_profile = OTPVerify.objects.create(user=user)
        otp_profile.set_email_otp(str(email_code))
        otp_profile.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token' : token.key, 'message': 'otp sent', 'next' : 'verify', 'email_otp' : email_code}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def otp_verification(request):
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        email_otp = request.data.get('email_otp')
        email = request.data.get('email')
        # set is_active to False at user creation if email auth is needed
        if not User.objects.filter(email=request.data.get('email'), is_active=False).exists():
            return Response({'detail' : 'error'}, status=403)
        user_otp = OTPVerify.objects.get(user=User.objects.get(email=request.data.get('email'), is_active=False))
        if not user_otp.verify_email(str(email_otp)):
            return Response({'detail' : 'otp mismatch'}, status=402)
        user_otp.save()

        user = user_otp.user
        user.username = email
        user.email = email
        user.is_active = True
        user.save()
        return Response({'detail' : 'verification successful', 'next' : 'setup'}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def google_login_and_signup(request):
    token = request.data.get('id_token')
    try:
        idinfo = id_token.verify_oauth2_token(token, Request())
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        user_email = idinfo['email']
    except ValueError:
        return Response({'error': 'Invalid token'}, status=400)
    
    try:
        if not User.objects.filter(username=user_email).exists():
            user = User.objects.create(email=user_email, username=user_email)
            preference = Preference.objects.create()
            question = Question.objects.create()
            location = Location.objects.create()
            profile = Profile.objects.create(
                user = user,
                location = location,
                question = question,
                preference = preference
            )
            left_swipe = LeftSwipe.objects.create(user=profile)
            otp_profile = OTPVerify.objects.create(user=user, is_email_verified = True)
        user = User.objects.get(username=user_email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)
    
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=400)
 
        
    